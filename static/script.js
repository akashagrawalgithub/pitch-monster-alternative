let recognition;
let isListening = false;
let isProcessing = false;
let speechTimeout;
let lastSpeechTime = 0;

// DOM elements
const voiceButton = document.getElementById("voiceButton");
const buttonText = document.getElementById("buttonText");
const status = document.getElementById("status");
const waveContainer = document.getElementById("waveContainer");
const conversation = document.getElementById("conversation");
const stopButton = document.getElementById("stopButton");

// Check for speech recognition support
if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    status.textContent = "Your browser does not support Web Speech API.";
    voiceButton.disabled = true;
}

function toggleListening() {
    if (isListening) {
        stopListening();
    } else {
        startListening();
    }
}

function startListening() {
    if (isProcessing) return;
    
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";
    recognition.interimResults = true; // Enable interim results
    recognition.maxAlternatives = 1;
    recognition.continuous = true;

    recognition.start();
    isListening = true;
    
    // Update UI
    voiceButton.classList.add('listening');
    buttonText.textContent = "Listening...";
    status.textContent = "Listening for your voice...";
    waveContainer.classList.add('active');
    stopButton.style.display = 'inline-block';

    let finalTranscript = '';
    let interimTranscript = '';

    recognition.onresult = function (event) {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
        }

        // Update status with interim results
        if (interimTranscript) {
            status.textContent = `Listening: "${interimTranscript}"...`;
            lastSpeechTime = Date.now();
        }

        // If we have final results, start the 3-second timer
        if (finalTranscript) {
            finalTranscript = finalTranscript.trim();
            if (finalTranscript.length > 0) {
                // Clear any existing timeout
                if (speechTimeout) {
                    clearTimeout(speechTimeout);
                }
                
                // Set 3-second timeout to process the complete speech
                speechTimeout = setTimeout(() => {
                    processUserInput(finalTranscript);
                }, 3000);
                
                status.textContent = `Captured: "${finalTranscript}" - Processing in 3 seconds...`;
            }
        }
    };

    recognition.onerror = function (event) {
        console.error("Speech recognition error:", event.error);
        if (event.error === 'no-speech') {
            status.textContent = "No speech detected. Try again.";
        } else {
            status.textContent = "Error: " + event.error;
        }
        
        isProcessing = false;
        
        // Restart recognition after a short delay
        if (isListening) {
            setTimeout(() => {
                if (isListening) recognition.start();
            }, 1000);
        }
    };

    recognition.onend = function () {
        if (isListening && !isProcessing) {
            // Restart recognition if it ended unexpectedly
            setTimeout(() => {
                if (isListening) recognition.start();
            }, 100);
        }
    };
}

function processUserInput(text) {
    if (isProcessing) return;
    isProcessing = true;
    
    // Clear the timeout since we're processing now
    if (speechTimeout) {
        clearTimeout(speechTimeout);
        speechTimeout = null;
    }
    
    // Add user message to conversation
    addMessage("You", text, "user-message");
    
    // Check for exit commands
    if (["stop", "end", "quit", "exit", "goodbye", "bye"].includes(text.toLowerCase().trim())) {
        addMessage("AI", "Goodbye! Have a great day!", "ai-message");
        speak("Goodbye! Have a great day!");
        stopListening();
        return;
    }

    // Show processing status
    status.innerHTML = '<span class="loading"></span> Processing complete speech...';
    
    // Send the complete user input to the server
    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
    })
    .then(response => response.json())
    .then(data => {
        if (data.reply) {
            addMessage("AI", data.reply, "ai-message");
            speak(data.reply);
        } else {
            addMessage("AI", "Sorry, I didn't get that. Could you repeat?", "ai-message");
            speak("Sorry, I didn't get that. Could you repeat?");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        addMessage("AI", "Sorry, there was an error. Please try again.", "ai-message");
        speak("Sorry, there was an error. Please try again.");
    })
    .finally(() => {
        isProcessing = false;
        status.textContent = "Listening for your voice...";
        
        // Restart recognition if still listening
        if (isListening) {
            setTimeout(() => {
                if (isListening) recognition.start();
            }, 100);
        }
    });
}

function stopListening() {
    if (recognition) {
        recognition.stop();
    }
    isListening = false;
    isProcessing = false;
    
    // Clear any pending timeout
    if (speechTimeout) {
        clearTimeout(speechTimeout);
        speechTimeout = null;
    }
    
    // Update UI
    voiceButton.classList.remove('listening');
    buttonText.textContent = "Start Talking";
    status.textContent = "Click the button to start voice chat";
    waveContainer.classList.remove('active');
    stopButton.style.display = 'none';
}

function addMessage(sender, content, className) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
    
    const labelDiv = document.createElement('div');
    labelDiv.className = 'message-label';
    labelDiv.textContent = sender;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(labelDiv);
    messageDiv.appendChild(contentDiv);
    
    conversation.appendChild(messageDiv);
    
    // Auto-scroll to bottom
    conversation.scrollTop = conversation.scrollHeight;
    
    // Limit conversation history to last 10 messages
    const messages = conversation.querySelectorAll('.message');
    if (messages.length > 20) {
        conversation.removeChild(messages[0]);
    }
}

function speak(text) {
    // Cancel any ongoing speech
    speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US";
    utterance.rate = 1.1; // Slightly faster speech
    utterance.pitch = 1.0;
    utterance.volume = 0.9;
    
    // Use a more natural voice if available
    const voices = speechSynthesis.getVoices();
    const preferredVoice = voices.find(voice => 
        voice.lang.includes('en') && 
        (voice.name.includes('Google') || voice.name.includes('Natural'))
    );
    if (preferredVoice) {
        utterance.voice = preferredVoice;
    }
    
    speechSynthesis.speak(utterance);
}

// Initialize speech synthesis voices
speechSynthesis.onvoiceschanged = function() {
    // Voices are now available
};

// Add keyboard shortcuts
document.addEventListener('keydown', function(event) {
    if (event.code === 'Space' && !event.target.matches('input, textarea')) {
        event.preventDefault();
        toggleListening();
    }
    
    if (event.code === 'Escape') {
        stopListening();
    }
});

// Add touch/click feedback
voiceButton.addEventListener('touchstart', function() {
    this.style.transform = 'scale(0.95)';
});

voiceButton.addEventListener('touchend', function() {
    this.style.transform = 'scale(1)';
});

// Auto-focus the voice button for better accessibility
window.addEventListener('load', function() {
    voiceButton.focus();
});
