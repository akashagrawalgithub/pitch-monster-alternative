// main.ts - Dynamic UI generation for Payment Follow-up Training
// --- UI Creation ---
function createUI() {
    document.body.style.background = '#f7f8fa';
    document.body.style.fontFamily = `'Inter', 'Segoe UI', Arial, sans-serif`;
    document.body.style.margin = '0';
    document.body.style.padding = '0';
    document.body.style.minHeight = '100vh';
    // Header
    const header = document.createElement('div');
    header.className = 'header';
    header.style.display = 'flex';
    header.style.alignItems = 'center';
    header.style.justifyContent = 'space-between';
    header.style.padding = '32px 40px 16px 40px';
    header.style.background = '#fff';
    header.style.borderBottom = '1px solid #ececec';
    const headerTitle = document.createElement('div');
    headerTitle.className = 'header-title';
    headerTitle.textContent = 'AI Voice Chat';
    headerTitle.style.fontSize = '1.5rem';
    headerTitle.style.fontWeight = '600';
    headerTitle.style.color = '#23272f';
    const headerTimer = document.createElement('div');
    headerTimer.className = 'header-timer';
    headerTimer.style.fontSize = '1.1rem';
    headerTimer.style.color = '#6b7280';
    headerTimer.style.display = 'flex';
    headerTimer.style.alignItems = 'center';
    headerTimer.style.gap = '8px';
    const timerEl = document.createElement('span');
    timerEl.id = 'timer';
    timerEl.textContent = '00:00';
    const dot = document.createElement('span');
    dot.textContent = '•';
    dot.style.fontSize = '1.2em';
    headerTimer.appendChild(timerEl);
    headerTimer.appendChild(dot);
    header.appendChild(headerTitle);
    header.appendChild(headerTimer);
    document.body.appendChild(header);
    // Main
    const main = document.createElement('div');
    main.className = 'main';
    main.style.display = 'flex';
    main.style.justifyContent = 'center';
    main.style.alignItems = 'flex-start';
    main.style.gap = '32px';
    main.style.padding = '40px 0';
    main.style.maxWidth = '1100px';
    main.style.margin = '0 auto';
    // Voice Controls Card
    const card1 = document.createElement('div');
    card1.className = 'card';
    card1.style.maxWidth = '340px';
    card1.style.background = '#fff';
    card1.style.borderRadius = '16px';
    card1.style.boxShadow = '0 2px 12px rgba(44,62,80,0.06)';
    card1.style.padding = '32px 28px';
    card1.style.minWidth = '340px';
    card1.style.minHeight = '320px';
    card1.style.display = 'flex';
    card1.style.flexDirection = 'column';
    const controlsTitle = document.createElement('div');
    controlsTitle.className = 'voice-controls-title';
    controlsTitle.textContent = 'Voice Controls';
    controlsTitle.style.fontSize = '1.1rem';
    controlsTitle.style.fontWeight = '500';
    controlsTitle.style.marginBottom = '24px';
    controlsTitle.style.color = '#23272f';
    const startBtn = document.createElement('button');
    startBtn.className = 'voice-btn';
    startBtn.id = 'startBtn';
    startBtn.textContent = '🎤 Start Recording';
    startBtn.style.width = '100%';
    startBtn.style.padding = '18px 0';
    startBtn.style.fontSize = '1.1rem';
    startBtn.style.fontWeight = '600';
    startBtn.style.border = 'none';
    startBtn.style.borderRadius = '8px';
    startBtn.style.background = '#2563eb';
    startBtn.style.color = '#fff';
    startBtn.style.marginBottom = '18px';
    startBtn.style.cursor = 'pointer';
    startBtn.style.transition = 'background 0.2s';
    const endBtn = document.createElement('button');
    endBtn.className = 'end-btn';
    endBtn.id = 'endBtn';
    endBtn.textContent = 'End Session';
    endBtn.style.width = '100%';
    endBtn.style.padding = '14px 0';
    endBtn.style.fontSize = '1rem';
    endBtn.style.fontWeight = '500';
    endBtn.style.border = 'none';
    endBtn.style.borderRadius = '8px';
    endBtn.style.background = '#e5e7eb';
    endBtn.style.color = '#23272f';
    endBtn.style.cursor = 'pointer';
    endBtn.style.transition = 'background 0.2s';
    card1.appendChild(controlsTitle);
    card1.appendChild(startBtn);
    card1.appendChild(endBtn);
    // Live Transcript Card
    const card2 = document.createElement('div');
    card2.className = 'card';
    card2.style.flex = '1';
    card2.style.background = '#fff';
    card2.style.borderRadius = '16px';
    card2.style.boxShadow = '0 2px 12px rgba(44,62,80,0.06)';
    card2.style.padding = '32px 28px';
    card2.style.display = 'flex';
    card2.style.flexDirection = 'column';
    const liveTitle = document.createElement('div');
    liveTitle.className = 'live-title';
    liveTitle.textContent = 'Live Transcript';
    liveTitle.style.fontSize = '1.1rem';
    liveTitle.style.fontWeight = '500';
    liveTitle.style.marginBottom = '24px';
    liveTitle.style.color = '#23272f';
    const transcriptList = document.createElement('div');
    transcriptList.className = 'transcript-list';
    transcriptList.id = 'transcriptList';
    transcriptList.style.flex = '1';
    transcriptList.style.overflowY = 'auto';
    transcriptList.style.paddingRight = '4px';
    card2.appendChild(liveTitle);
    card2.appendChild(transcriptList);
    main.appendChild(card1);
    main.appendChild(card2);
    document.body.appendChild(main);
    // Responsive styles
    const style = document.createElement('style');
    style.textContent = `
        @media (max-width: 900px) {
            .main { flex-direction: column !important; align-items: stretch !important; gap: 24px !important; padding: 24px 0 !important; }
            .card { min-width: unset !important; width: 100% !important; }
        }
    `;
    document.head.appendChild(style);
}
// --- Logic (same as before, but query elements after UI creation) ---
createUI();
let recognition = null;
let isListening = false;
let isProcessing = false;
let speechTimeout = null;
let timerInterval = null;
let secondsElapsed = 0;
let transcriptHistory = [];
let isRecognitionActive = false;
const startBtn = document.getElementById('startBtn');
const endBtn = document.getElementById('endBtn');
const timerEl = document.getElementById('timer');
const transcriptList = document.getElementById('transcriptList');
let currentSpeechAudio = null;
function formatTime(secs) {
    const m = Math.floor(secs / 60).toString().padStart(2, '0');
    const s = (secs % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
}
function startTimer() {
    secondsElapsed = 0;
    timerEl.textContent = formatTime(secondsElapsed);
    timerInterval = window.setInterval(() => {
        secondsElapsed++;
        timerEl.textContent = formatTime(secondsElapsed);
    }, 1000);
}
function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}
function addTranscript(sender, text) {
    const now = new Date();
    const time = formatTime(secondsElapsed);
    transcriptHistory.push({ sender, text, time });
    // Create transcript item
    const item = document.createElement('div');
    item.className = 'transcript-item';
    const avatar = document.createElement('div');
    avatar.className = 'transcript-avatar';
    avatar.textContent = sender === 'AI' ? '🤖' : '🧑';
    const content = document.createElement('div');
    content.className = 'transcript-content';
    content.textContent = text;
    const meta = document.createElement('div');
    meta.className = 'transcript-meta';
    meta.textContent = `${sender}  ${time}`;
    const contentWrap = document.createElement('div');
    contentWrap.appendChild(content);
    contentWrap.appendChild(meta);
    item.appendChild(avatar);
    item.appendChild(contentWrap);
    transcriptList.appendChild(item);
    transcriptList.scrollTop = transcriptList.scrollHeight;
}
function resetTranscript() {
    transcriptHistory = [];
    transcriptList.innerHTML = '';
}
function startListening() {
    if (isListening || isProcessing || isRecognitionActive)
        return;
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        alert('Your browser does not support Web Speech API.');
        return;
    }
    recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;
    recognition.continuous = true;
    isListening = true;
    isProcessing = false;
    let finalTranscript = '';
    recognition.onresult = (event) => {
        // Stop any ongoing AI speech as soon as user starts speaking
        if (window.speechSynthesis)
            window.speechSynthesis.cancel();
        let interim = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            }
            else {
                interim += transcript;
            }
        }
        if (currentSpeechAudio) {
            currentSpeechAudio.pause();
            currentSpeechAudio.currentTime = 0;
        }
        // If user is still speaking, reset the timer
        if (interim) {
            if (speechTimeout)
                clearTimeout(speechTimeout);
            speechTimeout = window.setTimeout(() => {
                if (finalTranscript.trim()) {
                    processUserInput(finalTranscript.trim());
                    finalTranscript = '';
                }
            }, 3000);
        }
        // If only final, start the 3s timer
        if (finalTranscript && !interim) {
            if (speechTimeout)
                clearTimeout(speechTimeout);
            speechTimeout = window.setTimeout(() => {
                if (finalTranscript.trim()) {
                    processUserInput(finalTranscript.trim());
                    finalTranscript = '';
                }
            }, 3000);
        }
    };
    recognition.onerror = (event) => {
        isListening = false;
        isProcessing = false;
        isRecognitionActive = false;
        recognition === null || recognition === void 0 ? void 0 : recognition.stop();
        alert('Speech recognition error: ' + event.error);
    };
    recognition.onstart = () => { isRecognitionActive = true; };
    recognition.onend = () => {
        isRecognitionActive = false;
        if (isListening && !isProcessing) {
            // Only restart if not already active
            if (!isRecognitionActive) {
                recognition === null || recognition === void 0 ? void 0 : recognition.start();
            }
        }
    };
    recognition.start();
}
function stopListening() {
    isListening = false;
    isProcessing = false;
    if (recognition && isRecognitionActive)
        recognition.stop();
    if (speechTimeout)
        clearTimeout(speechTimeout);
}
async function speak(text) {
    const response = await fetch('https://api.sws.speechify.com/v1/audio/speech', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer fsMaQJ15FuAGsz5jwm_qNR7V-gCZ8Jp-rZxq5Ytwh4s=',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            input: text,
            voice_id: 'steven',
            audio_format: 'mp3'
        })
    });
    const data = await response.json();
    playBase64Audio(data.audio_data, 'mp3');
}
function playBase64Audio(base64, format = 'mp3') {
    if (currentSpeechAudio) {
        currentSpeechAudio.pause();
        currentSpeechAudio.currentTime = 0;
    }
    currentSpeechAudio = new Audio(`data:audio/${format};base64,${base64}`);
    currentSpeechAudio.play();
}
function processUserInput(text) {
    if (isProcessing)
        return;
    isProcessing = true;
    addTranscript('You', text);
    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
    })
        .then(res => res.json())
        .then(data => {
        addTranscript('AI', data.reply);
        speak(data.reply); // AI speaks the reply
        isProcessing = false;
        // Do NOT call recognition.start() here; let onend handle it
    })
        .catch(err => {
        addTranscript('AI', 'Error: ' + err.message);
        isProcessing = false;
    });
}
startBtn.onclick = () => {
    resetTranscript();
    startTimer();
    const welcome = "Hello! Welcome to the Majestic Estates. How can I help you today?";
    addTranscript('AI', welcome);
    speak(welcome);
    startListening();
    startBtn.disabled = true;
    endBtn.disabled = false;
};
endBtn.onclick = () => {
    stopListening();
    stopTimer();
    startBtn.disabled = false;
    endBtn.disabled = true;
};
// Initial state
startBtn.disabled = false;
endBtn.disabled = true;
