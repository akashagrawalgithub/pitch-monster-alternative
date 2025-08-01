// main.ts - Dynamic UI generation for Payment Follow-up Training

// --- UI Creation ---
function createUI() {
    // Set up full-screen, immersive background with white and light blue gradient
    document.body.style.background = 'linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%)';
    document.body.style.fontFamily = `'Inter', 'Segoe UI', Arial, sans-serif`;
    document.body.style.margin = '0';
    document.body.style.padding = '0';
    document.body.style.minHeight = '100vh';
    document.body.style.overflow = 'hidden';

    // Top bar (minimal)
    const topBar = document.createElement('div');
    topBar.className = 'top-bar';
    topBar.style.position = 'fixed';
    topBar.style.top = '0';
    topBar.style.left = '0';
    topBar.style.width = '100vw';
    topBar.style.height = '60px';
    topBar.style.display = 'flex';
    topBar.style.alignItems = 'center';
    topBar.style.justifyContent = 'center';
    topBar.style.gap = '15px';
    topBar.style.padding = '0 18px';
    topBar.style.background = 'rgba(255,255,255,0.25)';
    topBar.style.backdropFilter = 'blur(12px)';
    topBar.style.zIndex = '100';
    topBar.style.boxShadow = '0 2px 16px rgba(44,62,80,0.07)';
    topBar.style.overflow = 'visible';

    const appTitle = document.createElement('div');
    appTitle.textContent = 'Import/Export Analytics Consultant';
    appTitle.style.fontSize = '18px';
    appTitle.style.fontWeight = '500';
    appTitle.style.letterSpacing = '0.5px';
    appTitle.style.color = '#23272f';
    appTitle.style.opacity = '0.92';
    appTitle.style.whiteSpace = 'nowrap';

    const timerWrap = document.createElement('div');
    timerWrap.style.display = 'flex';
    timerWrap.style.alignItems = 'center';
    timerWrap.style.gap = '8px';
    timerWrap.style.fontSize = '1.1rem';
    timerWrap.style.color = '#23272f';
    timerWrap.style.fontWeight = '500';
    timerWrap.style.opacity = '0.85';
    timerWrap.style.whiteSpace = 'nowrap';

    const timerEl = document.createElement('span');
    timerEl.id = 'timer';
    timerEl.textContent = '00:00';
    const dot = document.createElement('span');
    dot.id = 'recordingDot';
    dot.textContent = '•';
    dot.style.fontSize = '1.5em';
    dot.style.color = '#e11d48';
    dot.style.opacity = '0';
    dot.style.transition = 'opacity 0.3s';
    timerWrap.appendChild(timerEl);
    timerWrap.appendChild(dot);

    topBar.appendChild(appTitle);
    topBar.appendChild(timerWrap);
    document.body.appendChild(topBar);

    // Voice wave visualization area (full screen)
    const voiceWaveArea = document.createElement('div');
    voiceWaveArea.className = 'voice-wave-area';
    voiceWaveArea.id = 'voiceWaveArea';
    voiceWaveArea.style.position = 'fixed';
    voiceWaveArea.style.top = '60px';
    voiceWaveArea.style.left = '0';
    voiceWaveArea.style.width = '100vw';
    voiceWaveArea.style.height = 'calc(100vh - 60px)';
    voiceWaveArea.style.display = 'flex';
    voiceWaveArea.style.flexDirection = 'column';
    voiceWaveArea.style.justifyContent = 'center';
    voiceWaveArea.style.alignItems = 'center';
    voiceWaveArea.style.zIndex = '1';
    voiceWaveArea.style.background = 'transparent';

    // Voice wave container
    const voiceWaveContainer = document.createElement('div');
    voiceWaveContainer.className = 'voice-wave-container';
    voiceWaveContainer.id = 'voiceWaveContainer';
    voiceWaveContainer.style.display = 'flex';
    voiceWaveContainer.style.alignItems = 'center';
    voiceWaveContainer.style.justifyContent = 'center';
    voiceWaveContainer.style.gap = '4px';
    voiceWaveContainer.style.height = '60px';

    // Create voice wave bars
    for (let i = 0; i < 20; i++) {
        const bar = document.createElement('div');
        bar.className = 'voice-wave-bar';
        bar.style.width = '3px';
        bar.style.height = '4px';
        bar.style.background = 'rgba(37,99,235,0.3)';
        bar.style.borderRadius = '2px';
        bar.style.transition = 'height 0.1s ease';
        voiceWaveContainer.appendChild(bar);
    }

    voiceWaveArea.appendChild(voiceWaveContainer);
    document.body.appendChild(voiceWaveArea);

    // Hidden transcript storage (not visible)
    const hiddenTranscript = document.createElement('div');
    hiddenTranscript.id = 'hiddenTranscript';
    hiddenTranscript.style.display = 'none';
    document.body.appendChild(hiddenTranscript);

    // Floating mic button with ocean animation
    const micWrap = document.createElement('div');
    micWrap.className = 'mic-wrap';
    micWrap.style.position = 'fixed';
    micWrap.style.left = '50%';
    micWrap.style.bottom = '48px';
    micWrap.style.transform = 'translateX(-50%)';
    micWrap.style.zIndex = '20';
    micWrap.style.display = 'flex';
    micWrap.style.flexDirection = 'row';
    micWrap.style.alignItems = 'center';
    micWrap.style.gap = '24px';

    // Ocean animation (waves)
    const ocean = document.createElement('div');
    ocean.className = 'ocean-animation';
    ocean.style.position = 'absolute';
    ocean.style.left = '50%';
    ocean.style.top = '50%';
    ocean.style.transform = 'translate(-50%, -50%)';
    ocean.style.zIndex = '-1';
    ocean.style.pointerEvents = 'none';
    ocean.style.width = '160px';
    ocean.style.height = '160px';

    // Mic button with SVG icon (single button for start/stop)
    const micBtn = document.createElement('button');
    micBtn.className = 'voice-btn mic-btn';
    micBtn.id = 'micBtn';
    micBtn.innerHTML = '<span class="material-icons" style="font-size:20px;color:#fff;">mic</span>';
    micBtn.style.width = '50px';
    micBtn.style.height = '50px';
    micBtn.style.borderRadius = '50%';
    micBtn.style.background = 'rgba(37,99,235,0.95)';
    micBtn.style.color = '#fff';
    micBtn.style.border = 'none';
    micBtn.style.boxShadow = '0 8px 32px rgba(37,99,235,0.18), 0 2px 8px rgba(44,62,80,0.08)';
    micBtn.style.display = 'flex';
    micBtn.style.alignItems = 'center';
    micBtn.style.justifyContent = 'center';
    micBtn.style.fontWeight = '700';
    micBtn.style.fontSize = '1.3rem';
    micBtn.style.cursor = 'pointer';
    micBtn.style.transition = 'background 0.2s, box-shadow 0.2s, transform 0.2s';
    micBtn.style.position = 'relative';
    micBtn.style.outline = 'none';
    micBtn.style.visibility = 'visible';

    micWrap.appendChild(micBtn);
    micWrap.appendChild(ocean);
    document.body.appendChild(micWrap);

    // Load Material Icons font
    const materialIconsLink = document.createElement('link');
    materialIconsLink.rel = 'stylesheet';
    materialIconsLink.href = 'https://fonts.googleapis.com/icon?family=Material+Icons';
    document.head.appendChild(materialIconsLink);

    // Responsive and immersive styles, chat bubbles, ocean animation
    const style = document.createElement('style');
    style.textContent = `
        html, body {
            height: 100%;
            width: 100vw;
            overflow: hidden;
        }
        .top-bar {
            user-select: none;
            overflow: visible;
        }
        /* Voice wave animation */
        .voice-wave-bar {
            animation: voiceWave 1.5s ease-in-out infinite;
        }
        .voice-wave-bar:nth-child(odd) {
            animation-delay: 0.1s;
        }
        .voice-wave-bar:nth-child(even) {
            animation-delay: 0.2s;
        }
        .voice-wave-bar:nth-child(3n) {
            animation-delay: 0.3s;
        }
        .voice-wave-bar:nth-child(4n) {
            animation-delay: 0.4s;
        }
        .voice-wave-bar:nth-child(5n) {
            animation-delay: 0.5s;
        }
        @keyframes voiceWave {
            0%, 100% { height: 4px; opacity: 0.3; }
            50% { height: 40px; opacity: 0.8; }
        }
        /* Active voice wave when speaking */
        .voice-wave-bar.active {
            animation: activeVoiceWave 0.8s ease-in-out infinite;
        }
        @keyframes activeVoiceWave {
            0%, 100% { height: 8px; opacity: 0.4; }
            50% { height: 50px; opacity: 1; }
        }
        .mic-btn {
            box-shadow: 0 8px 32px rgba(37,99,235,0.18), 0 2px 8px rgba(44,62,80,0.08);
        }
        .mic-btn:active {
            transform: scale(0.96);
        }
        .mic-btn:not(:disabled):hover {
            background: #174bbd;
            box-shadow: 0 12px 36px rgba(37,99,235,0.22);
        }
        .end-btn {
            margin-left: 24px;
            box-shadow: 0 4px 16px rgba(229,39,76,0.13);
        }
        .end-btn:active {
            transform: scale(0.96);
        }
        .end-btn:not(:disabled):hover {
            background: #c81d4a;
            box-shadow: 0 8px 24px rgba(229,39,76,0.18);
        }
        .voice-btn:disabled, .end-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        #recordingDot.active {
            opacity: 1 !important;
            animation: pulse 1.2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.3; }
            100% { opacity: 1; }
        }
        @keyframes fadeInUp {
            0% { opacity: 0; transform: translateY(30px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        /* Ocean animation */
        .ocean-animation {
            pointer-events: none;
        }
        .ocean-animation .wave {
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            border-radius: 50%;
            opacity: 0.45;
            background: radial-gradient(circle, #a8edea 0%, #2563eb 100%);
            animation: waveAnim 2.5s infinite cubic-bezier(.23,1.01,.32,1);
        }
        .ocean-animation .wave.wave2 {
            opacity: 0.25;
            animation-delay: 1.2s;
        }
        @keyframes waveAnim {
            0% { width: 0; height: 0; opacity: 0.45; }
            70% { opacity: 0.18; }
            100% { width: 160px; height: 160px; opacity: 0; }
        }
        @media (max-width: 700px) {
            .top-bar { padding: 0 6px; height: 48px; }
            .transcript-bg { top: 48px; height: calc(100vh - 48px); }
            .mic-wrap { bottom: 18px; }
            .transcript-list { max-width: 98vw; padding: 0 2vw; }
        }
    `;
    document.head.appendChild(style);

    // Add ocean waves (hidden by default)
    function showOceanAnimation(active) {
        ocean.innerHTML = '';
        if (active) {
            for (let i = 0; i < 2; i++) {
                const wave = document.createElement('div');
                wave.className = 'wave' + (i === 1 ? ' wave2' : '');
                wave.style.width = '0px';
                wave.style.height = '0px';
                wave.style.background = 'radial-gradient(circle, #a8edea 0%, #2563eb 100%)';
                wave.style.position = 'absolute';
                wave.style.left = '50%';
                wave.style.top = '50%';
                wave.style.transform = 'translate(-50%, -50%)';
                ocean.appendChild(wave);
            }
        }
    }
    // Expose for use in setRecordingIndicator
    window['showOceanAnimation'] = showOceanAnimation;
}

// --- Logic (same as before, but query elements after UI creation) ---
createUI();

let recognition: any = null;
let isListening = false;
let isProcessing = false;
let speechTimeout: number | null = null;
let timerInterval: number | null = null;
let secondsElapsed = 0;
let transcriptHistory: { sender: 'AI' | 'You', text: string, time: string }[] = [];
let isRecognitionActive = false;
let audioQueue: string[] = [];
let isPlayingAudio = false;
let audioContext: AudioContext | null = null;
let audioBufferQueue: AudioBuffer[] = [];
let isAudioPlaying = false;
let currentSource: AudioBufferSourceNode | null = null;
let textChunks: string[] = [];
let isBuffering = false;
let finalTranscript = '';

const micBtn = document.getElementById('micBtn') as HTMLButtonElement;
const timerEl = document.getElementById('timer') as HTMLSpanElement;
const voiceWaveContainer = document.getElementById('voiceWaveContainer') as HTMLDivElement;
const hiddenTranscript = document.getElementById('hiddenTranscript') as HTMLDivElement;
let currentSpeechAudio: HTMLAudioElement | null = null;
function formatTime(secs: number): string {
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

function addTranscript(sender: 'AI' | 'You', text: string) {
    const time = formatTime(secondsElapsed);
    transcriptHistory.push({ sender, text, time });

    // Store in hidden transcript for later use
    const transcriptItem = document.createElement('div');
    transcriptItem.className = 'transcript-item ' + (sender === 'AI' ? 'ai' : 'you');
    transcriptItem.innerHTML = `
        <div class="transcript-avatar">${sender === 'AI' ? '🤖' : '🧑'}</div>
        <div class="transcript-content">${text}</div>
        <div class="transcript-meta">${sender}  ${time}</div>
    `;
    hiddenTranscript.appendChild(transcriptItem);
}

function resetTranscript() {
    transcriptHistory = [];
    hiddenTranscript.innerHTML = '';
}

function startListening() {
    if (isListening || isProcessing || isRecognitionActive) return;
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
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
    let interimBubble: { update: (text: string) => void, remove: () => void, getText: () => string } | null = null;

    recognition.onresult = (event: any) => {
        // Clear all outstanding audio when user starts speaking
        clearAllOutstandingAudio();

        let interim = '';
        let hasFinal = false;

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
                hasFinal = true;
            } else {
                interim += transcript;
            }
        }

        // Show interim transcript in real time
        if (interim && !hasFinal) {
            if (!interimBubble) {
                interimBubble = addStreamingTranscript('You');
            }
            interimBubble.update(interim);
            setVoiceWaveActive(true); // Activate voice wave when speaking
            
            // Clear any existing timeout when new speech is detected
            if (speechTimeout) {
                clearTimeout(speechTimeout);
                speechTimeout = null;
            }
        }

        // Process final transcript with 1-second delay to wait for complete thoughts
        if (hasFinal && finalTranscript.trim()) {
            // Clear any existing timeout
            if (speechTimeout) {
                clearTimeout(speechTimeout);
            }
            
            // Set a 1-second timeout to wait for user to complete their thought
            speechTimeout = window.setTimeout(() => {
                // Process the final transcript after the delay
                processUserInput(finalTranscript.trim());
                finalTranscript = '';
                speechTimeout = null;
                
                // Don't remove the interim bubble - let it stay for continuity
                // The interim bubble will continue to show new words as they come in
            }, 500); // 0.5 second delay
        }
    };

    recognition.onerror = (event: any) => {
        isListening = false;
        isProcessing = false;
        isRecognitionActive = false;
        recognition?.stop();
        alert('Speech recognition error: ' + event.error);
    };

    recognition.onstart = () => { isRecognitionActive = true; };

    recognition.onend = () => {
        isRecognitionActive = false;
        if (isListening && !isProcessing) {
            // Only restart if not already active
            if (!isRecognitionActive) {
                // Preserve the current interim transcript before restarting
                const currentInterimText = interimBubble ? interimBubble.getText() : '';
                
                recognition?.start();
                
                // If we had interim text, make sure it's preserved
                if (currentInterimText && interimBubble) {
                    // Small delay to ensure recognition has restarted
                    setTimeout(() => {
                        if (interimBubble) {
                            interimBubble.update(currentInterimText);
                        }
                    }, 100);
                }
            }
        }
    };

    recognition.start();
}

// Function to clear all outstanding audio
function clearAllOutstandingAudio() {
    // Stop any ongoing AI speech
    if (window.speechSynthesis) window.speechSynthesis.cancel();

    // Stop current audio source if playing
    if (currentSource) {
        try {
            currentSource.stop();
            currentSource.disconnect();
        } catch (e) {
            console.log('Audio source already stopped');
        }
        currentSource = null;
    }

    // Clear audio buffer queue
    audioBufferQueue = [];

    // Reset audio playing state
    isAudioPlaying = false;

    // Clear any remaining text chunks
    textChunks = [];

    // Stop buffering
    isBuffering = false;

    console.log('All outstanding audio cleared');
}

function stopListening() {
    console.log('Stopping listening...');
    isListening = false;
    isProcessing = false;
    isRecognitionActive = false;
    
    if (recognition) {
        try {
            recognition.stop();
        } catch (e) {
            console.log('Error stopping recognition:', e);
        }
    }
    
    // Clear speech timeout and process any pending final transcript immediately
    if (speechTimeout) {
        clearTimeout(speechTimeout);
        speechTimeout = null;
        
        // If there's pending final transcript, process it immediately when stopping
        if (finalTranscript && finalTranscript.trim()) {
            processUserInput(finalTranscript.trim());
            finalTranscript = '';
        }
    }
    
    console.log('Listening stopped');
}

async function speak(text: string) {
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

// New streaming speak function using Speechify's stream API
async function speakStream(text: string): Promise<void> {
    return new Promise((resolve, reject) => {
        fetch('https://api.sws.speechify.com/v1/audio/stream', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer fsMaQJ15FuAGsz5jwm_qNR7V-gCZ8Jp-rZxq5Ytwh4s=',
                'Accept': 'audio/mpeg',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                input: text,
                voice_id: 'steven'
            })
        }).then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            // Convert stream to blob and play
            response.blob().then(blob => {
                const audioUrl = URL.createObjectURL(blob);
                const audio = new Audio(audioUrl);

                audio.onended = () => {
                    URL.revokeObjectURL(audioUrl);
                    resolve();
                };

                audio.onerror = (err) => {
                    URL.revokeObjectURL(audioUrl);
                    reject(err);
                };

                audio.play().catch(reject);
            }).catch(reject);
        }).catch(reject);
    });
}

function playBase64Audio(base64: string, format: string = 'mp3') {
    if (currentSpeechAudio) {
        currentSpeechAudio.pause();
        currentSpeechAudio.currentTime = 0;
    }
    currentSpeechAudio = new Audio(`data:audio/${format};base64,${base64}`);
    currentSpeechAudio.play();
}

function processUserInput(text: string) {
    if (isProcessing) return;
    isProcessing = true;
    addTranscript('You', text);
    // Streaming version using /chat_stream and SSE
    const aiTranscript = addStreamingTranscript('AI');
    let fullReply = '';
    let textBuffer = '';

    fetchStreamedAIReply(text, (delta) => {
        fullReply += delta;
        aiTranscript.update(fullReply);

        // Add delta to text buffer
        textBuffer += delta;

        // Create chunks only at natural sentence boundaries
        if (shouldCreateChunk(textBuffer)) {
            const newChunks = splitIntoNaturalChunks(textBuffer);
            if (newChunks.length > 0) {
                textChunks.push(...newChunks);
                textBuffer = ''; // Clear buffer after splitting

                // Start buffering if not already
                if (!isBuffering) {
                    startPreBuffering();
                }
            }
        }
    }).then(() => {
        // Handle any remaining text
        if (textBuffer.trim()) {
            const remainingChunks = splitIntoNaturalChunks(textBuffer.trim());
            textChunks.push(...remainingChunks);
            if (!isBuffering) {
                startPreBuffering();
            }
        }
        
        // Add the complete AI response to transcript history
        if (fullReply.trim()) {
            addTranscript('AI', fullReply.trim());
        }
        
        isProcessing = false;
    }).catch(err => {
        aiTranscript.update('Error: ' + err.message);
        isProcessing = false;
    });
}

// Determine if we should create a chunk based only on natural sentence boundaries
function shouldCreateChunk(text: string): boolean {
    // Create chunk if we hit sentence boundaries (., !, ?)
    if (/[.?]\s*$/.test(text)) return true;

    // Create chunk if we have a natural pause (comma followed by space)
    if (/, \s*$/.test(text)) return true;

    return false;
}

// Split text into natural chunks (only at sentence boundaries)
function splitIntoNaturalChunks(text: string): string[] {
    const trimmedText = text.trim();
    if (!trimmedText) return [];

    // If the text ends with a sentence boundary, create a chunk
    if (/[.!?]\s*$/.test(trimmedText)) {
        return [trimmedText];
    }

    // If the text ends with a comma, create a chunk
    if (/, \s*$/.test(trimmedText)) {
        return [trimmedText];
    }

    // If no natural boundary, don't create a chunk yet
    return [];
}

// Add Speechify SDK script to the page
function loadSpeechifySDK() {
    const script = document.createElement('script');
    script.src = 'https://cdn.speechify.com/sdk/v1/speechify.js';
    script.onload = () => {
        console.log('Speechify SDK loaded');
        initializeSpeechify();
    };
    document.head.appendChild(script);
}

// Initialize Speechify SDK
function initializeSpeechify() {
    if (typeof (window as any).Speechify !== 'undefined') {
        (window as any).Speechify.init({
            apiKey: 'fsMaQJ15FuAGsz5jwm_qNR7V-gCZ8Jp-rZxq5Ytwh4s='
        });
    }
}

// Load SDK when page loads
loadSpeechifySDK();

// Replace the API-based audio function with SDK-based approach
async function getAudioBufferFromSpeechify(text: string): Promise<AudioBuffer> {
    return new Promise((resolve, reject) => {
        if (typeof (window as any).Speechify === 'undefined') {
            reject(new Error('Speechify SDK not loaded'));
            return;
        }

        (window as any).Speechify.speak({
            text: text,
            voice: 'steven',
            format: 'mp3',
            onStart: () => {
                console.log('Audio started for:', text);
            },
            onEnd: () => {
                console.log('Audio ended for:', text);
            },
            onError: (error: any) => {
                console.error('Speechify error:', error);
                reject(error);
            }
        }).then((audioBuffer: AudioBuffer) => {
            resolve(audioBuffer);
        }).catch(reject);
    });
}

// Alternative: Use SDK's streaming method for better sync
async function speakWithSDK(text: string): Promise<void> {
    return new Promise((resolve, reject) => {
        if (typeof (window as any).Speechify === 'undefined') {
            reject(new Error('Speechify SDK not loaded'));
            return;
        }

        (window as any).Speechify.stream({
            text: text,
            voice: 'steven',
            onChunk: (chunk: any) => {
                // Handle streaming audio chunks
                if (audioContext) {
                    audioContext.decodeAudioData(chunk).then(audioBuffer => {
                        audioBufferQueue.push(audioBuffer);

                        // Start playing immediately when we have the first audio buffer
                        if (audioBufferQueue.length === 1 && !isAudioPlaying) {
                            startContinuousAudioPlayback();
                        }
                    });
                }
            },
            onComplete: () => {
                resolve();
            },
            onError: (error: any) => {
                reject(error);
            }
        });
    });
}

// Update the pre-buffering system to use SDK
async function startPreBuffering() {
    if (isBuffering) return;
    isBuffering = true;

    while (textChunks.length > 0) {
        // Take up to 3 chunks for buffering
        const chunksToBuffer = textChunks.splice(0, 3);

        // Process chunks and start playing immediately when first is ready
        for (let i = 0; i < chunksToBuffer.length; i++) {
            const chunk = chunksToBuffer[i];
            try {
                await speakWithSDK(chunk);

                // Start playing immediately when we have the first audio buffer
                if (audioBufferQueue.length === 1 && !isAudioPlaying) {
                    startContinuousAudioPlayback();
                }
            } catch (err) {
                console.error('Speechify SDK error:', err);
                // Fallback to API if SDK fails
                try {
                    const audioBuffer = await getAudioBufferFromSpeechifyAPI(chunk);
                    audioBufferQueue.push(audioBuffer);

                    // Start playing immediately when we have the first audio buffer
                    if (audioBufferQueue.length === 1 && !isAudioPlaying) {
                        startContinuousAudioPlayback();
                    }
                } catch (apiErr) {
                    console.error('API fallback error:', apiErr);
                }
            }
        }

        // Reduced delay for SDK
        await new Promise(resolve => setTimeout(resolve, 20));
    }

    isBuffering = false;
}

// Keep the original API function as fallback
async function getAudioBufferFromSpeechifyAPI(text: string): Promise<AudioBuffer> {
    return new Promise((resolve, reject) => {
        fetch('https://api.sws.speechify.com/v1/audio/stream', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer fsMaQJ15FuAGsz5jwm_qNR7V-gCZ8Jp-rZxq5Ytwh4s=',
                'Accept': 'audio/mpeg',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                input: text,
                voice_id: 'steven'
            })
        }).then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            response.arrayBuffer().then(buffer => {
                if (!audioContext) {
                    audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
                }

                audioContext.decodeAudioData(buffer).then(resolve).catch(reject);
            }).catch(reject);
        }).catch(reject);
    });
}

function startContinuousAudioPlayback() {
    if (isAudioPlaying || audioBufferQueue.length === 0 || !audioContext) return;

    isAudioPlaying = true;
    playNextAudioBuffer();
}

function playNextAudioBuffer() {
    if (audioBufferQueue.length === 0) {
        isAudioPlaying = false;
        return;
    }

    const audioBuffer = audioBufferQueue.shift();
    if (!audioBuffer || !audioContext) return;

    currentSource = audioContext.createBufferSource();
    currentSource.buffer = audioBuffer;
    currentSource.connect(audioContext.destination);

    currentSource.onended = () => {
        // Immediately play next buffer if available
        if (audioBufferQueue.length > 0) {
            playNextAudioBuffer();
        } else {
            isAudioPlaying = false;
        }
    };

    currentSource.start();
}

// Helper to add a transcript item and allow updating its content (hidden)
function addStreamingTranscript(sender: 'AI' | 'You') {
    const time = formatTime(secondsElapsed);
    const item = document.createElement('div');
    item.className = 'transcript-item ' + (sender === 'AI' ? 'ai' : 'you');
    item.innerHTML = `
        <div class="transcript-avatar">${sender === 'AI' ? '🤖' : '🧑'}</div>
        <div class="transcript-content"></div>
        <div class="transcript-meta">${sender}  ${time}</div>
    `;
    
    const content = item.querySelector('.transcript-content') as HTMLDivElement;
    hiddenTranscript.appendChild(item);
    
    return {
        update: (text: string) => { 
            content.textContent = text; 
        },
        remove: () => { 
            // Don't remove the item - just clear its content
            content.textContent = '';
        },
        getText: () => content.textContent || ''
    };
}

// Fetch streaming AI reply from /chat_stream using SSE
function fetchStreamedAIReply(userText: string, onDelta: (delta: string) => void): Promise<void> {
    return new Promise((resolve, reject) => {
        const controller = new AbortController();
        fetch('/chat_stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userText }),
            signal: controller.signal
        }).then(response => {
            if (!response.body) throw new Error('No response body');
            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let buffer = '';
            function read() {
                reader.read().then(({ done, value }) => {
                    if (done) {
                        resolve();
                        return;
                    }
                    buffer += decoder.decode(value, { stream: true });
                    let lines = buffer.split(/\r?\n/);
                    buffer = lines.pop() || '';
                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            try {
                                const payload = JSON.parse(line.slice(6));
                                if (payload.reply) {
                                    onDelta(payload.reply);
                                }
                            } catch (e) {
                                // Ignore JSON parse errors
                            }
                        }
                    }
                    read();
                }).catch(reject);
            }
            read();
        }).catch(reject);
    });
}

function setRecordingIndicator(active) {
    const dot = document.getElementById('recordingDot');
    if (dot) {
        if (active) {
            dot.classList.add('active');
        } else {
            dot.classList.remove('active');
        }
    }
    if (window['showOceanAnimation']) {
        window['showOceanAnimation'](active);
    }
}

// Voice wave animation control
function setVoiceWaveActive(active: boolean) {
    const bars = voiceWaveContainer.querySelectorAll('.voice-wave-bar');
    bars.forEach(bar => {
        if (active) {
            bar.classList.add('active');
        } else {
            bar.classList.remove('active');
        }
    });
}

// Show final transcript in a modal
function showFinalTranscript() {
    // Create modal overlay
    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100vw';
    modal.style.height = '100vh';
    modal.style.background = 'rgba(0,0,0,0.8)';
    modal.style.zIndex = '1000';
    modal.style.display = 'flex';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.style.padding = '20px';

    // Create modal content
    const modalContent = document.createElement('div');
    modalContent.style.background = 'white';
    modalContent.style.borderRadius = '16px';
    modalContent.style.padding = '32px';
    modalContent.style.maxWidth = '800px';
    modalContent.style.maxHeight = '80vh';
    modalContent.style.overflowY = 'auto';
    modalContent.style.boxShadow = '0 20px 60px rgba(0,0,0,0.3)';

    // Create transcript content
    const transcriptContent = document.createElement('div');
    transcriptContent.innerHTML = `
        <h2 style="margin: 0 0 24px 0; color: #23272f; font-size: 24px; font-weight: 600;">Conversation Transcript</h2>
        <div style="display: flex; flex-direction: column; gap: 16px;">
            ${transcriptHistory.map(item => `
                <div style="display: flex; gap: 12px; align-items: flex-start;">
                    <div style="width: 32px; height: 32px; border-radius: 50%; background: ${item.sender === 'AI' ? '#e0e7ef' : '#fbeee0'}; display: flex; align-items: center; justify-content: center; font-size: 16px; color: ${item.sender === 'AI' ? '#2563eb' : '#eab308'}; flex-shrink: 0;">
                        ${item.sender === 'AI' ? '🤖' : '🧑'}
                    </div>
                    <div style="flex: 1;">
                        <div style="background: ${item.sender === 'AI' ? '#f8fafc' : '#fefefe'}; border: 1px solid ${item.sender === 'AI' ? '#e2e8f0' : '#f1f5f9'}; border-radius: 12px; padding: 16px; margin-bottom: 4px;">
                            ${item.text}
                        </div>
                        <div style="font-size: 12px; color: #64748b; text-align: right;">
                            ${item.sender} • ${item.time}
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
        <div style="margin-top: 24px; text-align: center;">
            <button onclick="this.closest('.modal-overlay').remove()" style="background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: 500;">
                Close Transcript
            </button>
        </div>
    `;

    modalContent.appendChild(transcriptContent);
    modal.appendChild(modalContent);
    modal.className = 'modal-overlay';
    document.body.appendChild(modal);

    // Close modal when clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
}

let isChatActive = false;
const micIcon = '<span class="material-icons" style="font-size:1.3em;color:#fff;">mic</span>';
const micOffIcon = '<span class="material-icons" style="font-size:1.3em;color:#fff;">mic_off</span>';

micBtn.onclick = () => {
    if (!isChatActive) {
        // Start chat
        resetTranscript();
        startTimer();
        setVoiceWaveActive(true); // Activate voice wave animation
        const welcome = "Hello! How can I help you today?";
        addTranscript('AI', welcome);
        speak(welcome);
        startListening();
        micBtn.innerHTML = micOffIcon;
        micBtn.style.background = 'rgba(229,39,76,0.92)';
        isChatActive = true;
    } else {
        // Stop chat
        clearAllOutstandingAudio(); // Clear all outstanding voice/audio
        stopListening();
        stopTimer();
        setVoiceWaveActive(false); // Deactivate voice wave animation
        micBtn.innerHTML = micIcon;
        micBtn.style.background = 'rgba(37,99,235,0.95)';
        isChatActive = false;
        
        // Show final transcript after a short delay
        setTimeout(() => {
            if (transcriptHistory.length > 0) {
                showFinalTranscript();
            }
        }, 500);
    }
};

// Initial state
micBtn.innerHTML = micIcon;
micBtn.style.background = 'rgba(37,99,235,0.95)';
isChatActive = false;
setRecordingIndicator(false); 