
function checkAuth() {
    // Simple check for authentication using local storage
    const isAuthenticated = localStorage.getItem('authenticated') === 'true';
    
    if (!isAuthenticated) {
        window.location.href = '/login.html';
        return false;
    }
    return true;
}

// --- Rules Popup ---
function createRulesPopup() {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.id = 'rulesOverlay';
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100vw';
    overlay.style.height = '100vh';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    overlay.style.display = 'flex';
    overlay.style.alignItems = 'center';
    overlay.style.justifyContent = 'center';
    overlay.style.zIndex = '10000';
    overlay.style.pointerEvents = 'auto';

    // Create popup container
    const popup = document.createElement('div');
    popup.style.background = '#ffffff';
    popup.style.borderRadius = '16px';
    popup.style.padding = '32px';
    popup.style.maxWidth = '500px';
    popup.style.width = '90%';
    popup.style.boxShadow = '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)';
    popup.style.border = '1px solid #e2e8f0';
    popup.style.position = 'relative';

    // Create title
    const title = document.createElement('h2');
    title.innerHTML = 'Hey 👋 Please take a look at the rules for role-play done right.';
    title.style.fontSize = '20px';
    title.style.fontWeight = '700';
    title.style.color = '#1e293b';
    title.style.marginBottom = '24px';
    title.style.lineHeight = '1.4';

    // Create rules list
    const rulesList = document.createElement('ul');
    rulesList.style.listStyle = 'none';
    rulesList.style.padding = '0';
    rulesList.style.margin = '0 0 24px 0';

    const rules = [
        'Wear headphones and speak clearly. Don\'t forget to smile 😊',
        'First response can be bit delayed, please wait for AI to respond.',
        'As soon as you finish recording, it will be sent for analysis and feedback. Take this attempt seriously!',
        'Find a quiet place and ensure that your microphone works properly.',
        'Speak confidently and avoid rushing. When you finish talking, click the "Stop" icon to end the role-play',
    ];

    rules.forEach(rule => {
        const li = document.createElement('li');
        li.style.display = 'flex';
        li.style.alignItems = 'flex-start';
        li.style.gap = '12px';
        li.style.marginBottom = '16px';
        li.style.fontSize = '15px';
        li.style.lineHeight = '1.6';
        li.style.color = '#475569';

        const bullet = document.createElement('span');
        bullet.innerHTML = '•';
        bullet.style.color = '#8b5cf6';
        bullet.style.fontWeight = 'bold';
        bullet.style.fontSize = '18px';
        bullet.style.lineHeight = '1.2';

        const text = document.createElement('span');
        text.textContent = rule;

        li.appendChild(bullet);
        li.appendChild(text);
        rulesList.appendChild(li);
    });

    // Create conclusion
    const conclusion = document.createElement('p');
    conclusion.innerHTML = 'Let\'s go 🚀';
    conclusion.style.fontSize = '16px';
    conclusion.style.fontWeight = '700';
    conclusion.style.color = '#1e293b';
    conclusion.style.marginBottom = '24px';
    conclusion.style.marginTop = '0';

    // Create agree button (initially disabled)
    const agreeButton = document.createElement('button');
    agreeButton.textContent = 'I agree';
    agreeButton.id = 'agreeButton';
    agreeButton.style.background = '#e2e8f0';
    agreeButton.style.color = '#64748b';
    agreeButton.style.border = 'none';
    agreeButton.style.borderRadius = '12px';
    agreeButton.style.padding = '14px 24px';
    agreeButton.style.fontSize = '16px';
    agreeButton.style.fontWeight = '600';
    agreeButton.style.cursor = 'not-allowed';
    agreeButton.style.width = '100%';
    agreeButton.style.transition = 'all 0.2s';
    agreeButton.disabled = true;

    // Add elements to popup
    popup.appendChild(title);
    popup.appendChild(rulesList);
    popup.appendChild(conclusion);
    popup.appendChild(agreeButton);

    // Add popup to overlay
    overlay.appendChild(popup);

    // Add overlay to body
    document.body.appendChild(overlay);

    // Enable button after 5 seconds
    setTimeout(() => {
        agreeButton.style.background = 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)';
        agreeButton.style.color = 'white';
        agreeButton.style.cursor = 'pointer';
        agreeButton.disabled = false;
        agreeButton.style.boxShadow = '0 4px 12px rgba(139, 92, 246, 0.3)';
    }, 10000);

    // Handle agree button click
    agreeButton.addEventListener('click', () => {
        if (!agreeButton.disabled) {
            overlay.remove();
        }
    });

    // Prevent closing on overlay click
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            // Do nothing - prevent closing
        }
    });
}

// --- UI Creation ---
function createUI() {
    // Set up full-screen, immersive background with white and light blue gradient
    document.body.style.background = 'linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%)';
    document.body.style.fontFamily = `'Inter', 'Segoe UI', Arial, sans-serif`;
    document.body.style.margin = '0';
    document.body.style.padding = '0';
    document.body.style.minHeight = '100vh';
    document.body.style.overflow = 'hidden';

    // Create and show rules popup
    createRulesPopup();

    // Top bar (minimal)
    const topBar = document.createElement('div');
    topBar.className = 'top-bar';
    topBar.style.position = 'fixed';
    topBar.style.top = '0';
    topBar.style.left = '0';
    topBar.style.width = '100vw';
    topBar.style.height = '50px';
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

    // Back button
    const backButton = document.createElement('button');
    backButton.innerHTML = '← Back to details';
    backButton.style.position = 'fixed';
    backButton.style.top = '8px';
    backButton.style.left = '18px';
    backButton.style.background = 'rgba(255,255,255,0.9)';
    backButton.style.border = '1px solid rgba(0,0,0,0.1)';
    backButton.style.borderRadius = '8px';
    backButton.style.padding = '6px 12px';
    backButton.style.fontSize = '13px';
    backButton.style.fontWeight = '500';
    backButton.style.color = '#374151';
    backButton.style.cursor = 'pointer';
    backButton.style.transition = 'all 0.2s';
    backButton.style.zIndex = '200';
    backButton.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
    backButton.onclick = () => window.location.href = '/agent-info.html';
    backButton.onmouseover = () => {
        backButton.style.background = 'rgba(255,255,255,0.95)';
        backButton.style.transform = 'translateY(-1px)';
    };
    backButton.onmouseout = () => {
        backButton.style.background = 'rgba(255,255,255,0.9)';
        backButton.style.transform = 'translateY(0)';
    };

    // Get agent type from localStorage and set appropriate title
    const agentType = localStorage.getItem('selectedAgentType') || 'payment-followup';
    const agentTitles = {
        'payment-followup': 'Payment Follow-up Training',
        'competitor-objection': 'Competitor Objection Training',
        'lead-to-demo': 'Lead to Demo Training',
        'closing-skills': 'Closing Skills Training',
        'cold-calling': 'Cold Calling Training',
        'discovery-call': 'Discovery Call Training'
    };
    
    const appTitle = document.createElement('div');
    appTitle.textContent = agentTitles[agentType] || 'Sales Training';
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

    topBar.appendChild(backButton);
    topBar.appendChild(appTitle);
    topBar.appendChild(timerWrap);
    document.body.appendChild(topBar);

    // Voice wave visualization area (full screen)
    const voiceWaveArea = document.createElement('div');
    voiceWaveArea.className = 'voice-wave-area';
    voiceWaveArea.id = 'voiceWaveArea';
    voiceWaveArea.style.position = 'fixed';
    voiceWaveArea.style.top = '50px';
    voiceWaveArea.style.left = '0';
    voiceWaveArea.style.width = '100vw';
    voiceWaveArea.style.height = 'calc(100vh - 50px)';
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
    function showOceanAnimation(active: boolean) {
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
    (window as any)['showOceanAnimation'] = showOceanAnimation;
}

// --- Logic (same as before, but query elements after UI creation) ---
// Check authentication before creating UI
if (checkAuth()) {
    createUI();
} else {
    // If not authenticated, the checkAuth function will redirect to login
    // This is just a fallback
    window.location.href = '/login.html';
}

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
let audioPlaybackQueue: ArrayBuffer[] = [];
let isPlayingQueue = false;
let currentSource: AudioBufferSourceNode | null = null;
let textChunks: string[] = [];
let isBuffering = false;
let finalTranscript = '';

// Audio recording variables
let mediaRecorder: MediaRecorder | null = null;
let audioChunks: Blob[] = [];
let isRecording = false;
let recordingStream: MediaStream | null = null;
let recordingStartTime = 0;
let audioDestination: MediaStreamAudioDestinationNode | null = null;
let audioSource: MediaStreamAudioSourceNode | null = null;

const micBtn = document.getElementById('micBtn') as HTMLButtonElement;
const timerEl = document.getElementById('timer') as HTMLSpanElement;
const voiceWaveContainer = document.getElementById('voiceWaveContainer') as HTMLDivElement;
const hiddenTranscript = document.getElementById('hiddenTranscript') as HTMLDivElement;
let currentSpeechAudio: HTMLAudioElement | null = null;
let accumulatedSpeech = '';
let lastSpeechTime = 0;

function formatTime(secs: number): string {
    const m = Math.floor(secs / 60).toString().padStart(2, '0');
    const s = (secs % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
}

function startTimer() {
    secondsElapsed = 0;
    sessionStorage.setItem('callStartTime', new Date().toISOString());
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
    
    // Configure for better speech capture
    if ('webkitSpeechRecognition' in window) {
        (recognition as any).continuous = true;
        (recognition as any).interimResults = true;
        (recognition as any).maxAlternatives = 1;
    }
    
    isListening = true;
    isProcessing = false;
    let finalTranscript = '';
    accumulatedSpeech = '';
    lastSpeechTime = 0;
    let interimBubble: { update: (text: string) => void, remove: () => void, getText: () => string } | null = null;
    let isUserSpeaking = false;
    let speechPauseTimeout: number | null = null;

    recognition.onresult = (event: any) => {
        // Clear audio playback immediately when user starts speaking
        clearAudioPlaybackOnly();
        
        // Handle user interruption (recording continues)
        handleUserInterruption();

        let interim = '';
        let hasFinal = false;

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
                accumulatedSpeech += transcript;
                hasFinal = true;
                lastSpeechTime = Date.now();
            } else {
                interim += transcript;
            }
        }

        // Show interim transcript in real time
        if (interim && !hasFinal) {
            if (!interimBubble) {
                interimBubble = addStreamingTranscript('You');
            }
            // Combine accumulated speech with current interim for better display
            const combinedInterim = (accumulatedSpeech + ' ' + interim).trim();
            interimBubble.update(combinedInterim);
            setVoiceWaveActive(true);
            isUserSpeaking = true;
            
            // Clear any existing timeout when new speech is detected
            if (speechTimeout) {
                clearTimeout(speechTimeout);
                speechTimeout = null;
            }
            if (speechPauseTimeout) {
                clearTimeout(speechPauseTimeout);
                speechPauseTimeout = null;
            }
        }

        // Handle final transcript - accumulate but don't process immediately
        if (hasFinal && finalTranscript.trim()) {
            // Clear any existing timeout
            if (speechTimeout) {
                clearTimeout(speechTimeout);
            }
            
            // Set a 1 second pause detection timeout for conversational flow
            speechPauseTimeout = window.setTimeout(() => {
                if (finalTranscript.trim().length > 0) {
                    // Use the most complete speech available
                    const speechToProcess = finalTranscript.trim();
                    finalTranscript = '';
                    
                    if (speechToProcess.length > 0) {
                        processUserInput(speechToProcess);
                        accumulatedSpeech = '';
                        // Clear any interim bubble to prevent duplicate processing
                        const interimBubbleElement = document.querySelector('.transcript-item.you .transcript-content') as HTMLDivElement;
                        if (interimBubbleElement) {
                            interimBubbleElement.textContent = '';
                        }
                    }
                }
                speechPauseTimeout = null;
                isUserSpeaking = false;
            }, 1000); // Wait 1 second of silence before processing
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
            // Restart recognition immediately if we're still supposed to be listening
            if (!isRecognitionActive && isListening) {
                // Preserve the current interim transcript before restarting
                const currentInterimText = interimBubble ? interimBubble.getText() : '';
                const currentFinalText = finalTranscript;
                const currentAccumulatedSpeech = accumulatedSpeech;
                
                // Restart immediately to avoid gaps in speech capture
                setTimeout(() => {
                    if (isListening && !isRecognitionActive) {
                        recognition?.start();
                        
                        // Restore interim text if we had one
                        if (currentInterimText && interimBubble) {
                            setTimeout(() => {
                                if (interimBubble) {
                                    interimBubble.update(currentInterimText);
                                }
                            }, 50);
                        }
                        
                        // Restore final transcript and accumulated speech if we had any
                        if (currentFinalText) {
                            finalTranscript = currentFinalText;
                        }
                        if (currentAccumulatedSpeech) {
                            accumulatedSpeech = currentAccumulatedSpeech;
                        }
                    }
                }, 50); // Minimal delay to restart recognition
            }
        }
    };

    recognition.start();
}

// Function to clear only audio playback (not speech recognition)
function clearAudioPlaybackOnly() {
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
    audioPlaybackQueue = [];

    // Reset audio playing state
    isAudioPlaying = false;
    isPlayingQueue = false;

    console.log('Audio playback cleared');
}

// Function to handle user interruption (no longer stops recording)
function handleUserInterruption() {
    console.log('User interrupted AI, continuing recording');
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
    audioPlaybackQueue = [];

    // Reset audio playing state
    isAudioPlaying = false;
    isPlayingQueue = false;

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
    
    // Clear all timeouts
    if (speechTimeout) {
        clearTimeout(speechTimeout);
        speechTimeout = null;
    }
    
    // Process any remaining speech immediately (only if not already processed)
    let speechToProcess = '';
    
    // Only process if we have unprocessed speech
    if (accumulatedSpeech.trim() || finalTranscript.trim()) {
        // Combine all available speech data
        const allSpeech: string[] = [];
        if (accumulatedSpeech && accumulatedSpeech.trim()) {
            allSpeech.push(accumulatedSpeech.trim());
        }
        if (finalTranscript && finalTranscript.trim()) {
            allSpeech.push(finalTranscript.trim());
        }
        
        // Check for interim text
        const interimBubbleElement = document.querySelector('.transcript-item.you .transcript-content') as HTMLDivElement;
        if (interimBubbleElement && interimBubbleElement.textContent && interimBubbleElement.textContent.trim()) {
            const interimText = interimBubbleElement.textContent.trim();
            if (interimText.length > 0) {
                allSpeech.push(interimText);
            }
        }
        
        // Combine all speech and remove duplicates, ensuring complete capture
        if (allSpeech.length > 0) {
            // Remove duplicates while preserving order and getting the most complete version
            const uniqueSpeech = allSpeech.filter((item, index) => allSpeech.indexOf(item) === index);
            speechToProcess = uniqueSpeech.join(' ').replace(/\s+/g, ' ').trim();
            console.log('Processing complete speech on stop:', speechToProcess);
            
            if (speechToProcess.length > 0) {
                processUserInput(speechToProcess);
            }
        }
    }
    
    // Clear all speech data
    finalTranscript = '';
    accumulatedSpeech = '';
    const interimBubbleElement = document.querySelector('.transcript-item.you .transcript-content') as HTMLDivElement;
    if (interimBubbleElement) {
        interimBubbleElement.textContent = '';
    }
    
    console.log('Listening stopped');
}

// Cartesia TTS functions
async function speak(text: string) {
    try {
        const response = await fetch('/tts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        await playBase64Audio(data.audio_data, 'pcm_f32le', data.sample_rate);
    } catch (error) {
        console.error('Cartesia TTS error:', error);
        // Fallback to browser speech synthesis
        if (window.speechSynthesis) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.9;
            utterance.pitch = 1.0;
            
            // For browser speech synthesis, we need to capture it differently
            // since it doesn't go through our audio context
            if (isRecording) {
                console.log('Using browser speech synthesis - audio will be captured via microphone');
            }
            
            window.speechSynthesis.speak(utterance);
        }
    }
}

// Streaming TTS using Cartesia
async function speakStream(text: string): Promise<void> {
    return new Promise((resolve, reject) => {
        fetch('/tts_stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        }).then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const reader = response.body?.getReader();
            const decoder = new TextDecoder('utf-8');
            let buffer = '';
            let audioChunks: Uint8Array[] = [];

            async function read() {
                try {
                    const { done, value } = await reader!.read();
                    if (done) {
                        // Combine all audio chunks and play
                        if (audioChunks.length > 0) {
                            const combinedAudio = new Uint8Array(audioChunks.reduce((acc, chunk) => acc + chunk.length, 0));
                            let offset = 0;
                            for (const chunk of audioChunks) {
                                combinedAudio.set(chunk, offset);
                                offset += chunk.length;
                            }
                            await playAudioBuffer(combinedAudio.buffer, 44100);
                        }
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
                                if (payload.audio_chunk) {
                                    const audioData = Uint8Array.from(atob(payload.audio_chunk), c => c.charCodeAt(0));
                                    audioChunks.push(audioData);
                                } else if (payload.status === 'complete') {
                                    // Audio streaming complete
                                } else if (payload.error) {
                                    reject(new Error(payload.error));
                                }
                            } catch (e) {
                                // Ignore JSON parse errors
                            }
                        }
                    }
                    read();
                } catch (error) {
                    reject(error);
                }
            }
            read();
        }).catch(reject);
    });
}

async function playBase64Audio(base64: string, _format: string = 'pcm_f32le', sampleRate: number = 44100) {
    if (currentSpeechAudio) {
        currentSpeechAudio.pause();
        currentSpeechAudio.currentTime = 0;
    }
    
    // Convert base64 to audio buffer and play
    const audioData = Uint8Array.from(atob(base64), c => c.charCodeAt(0));
    await playAudioBuffer(audioData.buffer, sampleRate);
}

async function playAudioBuffer(buffer: ArrayBuffer, sampleRate: number) {
    if (!audioContext) {
        audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    }

    // Resume audio context if it's suspended (required for autoplay policies)
    if (audioContext.state === 'suspended') {
        try {
            await audioContext.resume();
        } catch (error) {
            console.error('Failed to resume audio context:', error);
            return;
        }
    }

    try {
        // For raw PCM data, we need to create an AudioBuffer manually
        const audioBuffer = audioContext.createBuffer(1, buffer.byteLength / 4, sampleRate); // 4 bytes per float32
        const channelData = audioBuffer.getChannelData(0);
        
        // Copy the PCM data to the audio buffer
        const view = new Float32Array(buffer);
        channelData.set(view);
        
        if (currentSource) {
            currentSource.stop();
            currentSource.disconnect();
        }

        currentSource = audioContext.createBufferSource();
        currentSource.buffer = audioBuffer;
        
        // Connect to both speakers and recording destination
        currentSource.connect(audioContext.destination);
        if (audioDestination && isRecording) {
            currentSource.connect(audioDestination);
        }
        
        currentSource.start();
        
        console.log('Raw PCM audio playback started successfully');
    } catch (error) {
        console.error('Error playing raw PCM audio:', error);
    }
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
    if (/[.!?]\s*$/.test(text)) return true;

    // Create chunk if we have a natural pause (comma followed by space)
    if (/, \s*$/.test(text)) return true;

    // Create chunk if we have a substantial amount of text (prevent very long chunks)
    if (text.length > 150) return true; // Reduced from 200 to 150 for faster processing

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

    // If text is very long, split at the last sentence boundary
    if (trimmedText.length > 150) { // Reduced from 200 to 150
        const lastSentenceMatch = trimmedText.match(/.*[.!?]\s*$/);
        if (lastSentenceMatch) {
            return [lastSentenceMatch[0].trim()];
        }
    }

    // If no natural boundary, don't create a chunk yet
    return [];
}

// Audio queue system for sequential playback

async function playNextInQueue() {
    if (audioPlaybackQueue.length === 0 || isPlayingQueue) return;
    
    isPlayingQueue = true;
    
    while (audioPlaybackQueue.length > 0) {
        const audioBuffer = audioPlaybackQueue.shift()!;
        try {
            await playAudioBuffer(audioBuffer, 44100);
            
            // Wait for audio to finish before playing next
            if (currentSource) {
                await new Promise<void>((resolve) => {
                    currentSource!.onended = () => resolve();
                });
            }
        } catch (error) {
            console.error('Error playing audio from queue:', error);
        }
    }
    
    isPlayingQueue = false;
    
    // Check if AI has finished speaking after queue is empty
    setTimeout(() => {
        checkAIFinishedSpeaking();
    }, 500);
}

// Update the pre-buffering system to use Cartesia with proper queuing
async function startPreBuffering() {
    if (isBuffering) return;
    isBuffering = true;

    while (textChunks.length > 0) {
        // Take up to 2 chunks for buffering (reduced from 3 for faster processing)
        const chunksToBuffer = textChunks.splice(0, 2);

        // Process chunks and add to audio queue
        for (let i = 0; i < chunksToBuffer.length; i++) {
            const chunk = chunksToBuffer[i];
            try {
                // Get audio data and add to queue instead of playing immediately
                const audioBuffer = await getAudioBuffer(chunk);
                audioPlaybackQueue.push(audioBuffer);
                
                // Start playing queue if not already playing
                if (!isPlayingQueue) {
                    playNextInQueue();
                }
            } catch (err) {
                console.error('Cartesia TTS error:', err);
                // Fallback to simple speak function
                try {
                    await speak(chunk);
                } catch (fallbackErr) {
                    console.error('Fallback TTS error:', fallbackErr);
                }
            }
        }
    }

    isBuffering = false;
}

// Function to check if AI has finished speaking (no longer stops recording)
function checkAIFinishedSpeaking() {
    if (!isBuffering && audioPlaybackQueue.length === 0 && !isPlayingQueue) {
        console.log('AI finished speaking, recording continues');
    }
}

// Helper function to get audio buffer without playing
async function getAudioBuffer(text: string): Promise<ArrayBuffer> {
    return new Promise((resolve, reject) => {
        fetch('/tts_stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        }).then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const reader = response.body?.getReader();
            const decoder = new TextDecoder('utf-8');
            let buffer = '';
            let audioChunks: Uint8Array[] = [];

            async function read() {
                try {
                    const { done, value } = await reader!.read();
                    if (done) {
                        // Combine all audio chunks and return buffer
                        if (audioChunks.length > 0) {
                            const combinedAudio = new Uint8Array(audioChunks.reduce((acc, chunk) => acc + chunk.length, 0));
                            let offset = 0;
                            for (const chunk of audioChunks) {
                                combinedAudio.set(chunk, offset);
                                offset += chunk.length;
                            }
                            resolve(combinedAudio.buffer);
                        } else {
                            reject(new Error('No audio data received'));
                        }
                        return;
                    }

                    buffer += decoder.decode(value, { stream: true });
                    let lines = buffer.split(/\r?\n/);
                    buffer = lines.pop() || '';

                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            try {
                                const payload = JSON.parse(line.slice(6));
                                if (payload.audio_chunk) {
                                    const audioData = Uint8Array.from(atob(payload.audio_chunk), c => c.charCodeAt(0));
                                    audioChunks.push(audioData);
                                } else if (payload.status === 'complete') {
                                    // Audio streaming complete
                                } else if (payload.error) {
                                    reject(new Error(payload.error));
                                }
                            } catch (e) {
                                // Ignore JSON parse errors
                            }
                        }
                    }
                    read();
                } catch (error) {
                    reject(error);
                }
            }
            read();
        }).catch(reject);
    });
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
        
        // Get the selected agent type from localStorage
        const agentType = localStorage.getItem('selectedAgentType') || 'discovery-call';
        
        // Generate a unique session ID for this conversation
        const sessionId = localStorage.getItem('currentSessionId') || generateSessionId();
        localStorage.setItem('currentSessionId', sessionId);
        
        fetch('/chat_stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message: userText,
                agent_type: agentType,
                session_id: sessionId
            }),
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

function setRecordingIndicator(active: boolean) {
    const dot = document.getElementById('recordingDot');
    if (dot) {
        if (active) {
            dot.classList.add('active');
        } else {
            dot.classList.remove('active');
        }
    }
    if ((window as any)['showOceanAnimation']) {
        (window as any)['showOceanAnimation'](active);
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

// Start audio recording
async function startAudioRecording() {
    try {
        // Get user's microphone stream
        const userStream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true,
                sampleRate: 44100
            } 
        });
        
        // Store the stream for cleanup
        recordingStream = userStream;
        
        // Create audio context for mixing user and AI audio
        if (!audioContext) {
            audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
        }
        
        // Create audio destination to capture all audio
        audioDestination = audioContext.createMediaStreamDestination();
        
        // Create source from user's microphone
        audioSource = audioContext.createMediaStreamSource(userStream);
        audioSource.connect(audioDestination);
        
        // Try different MIME types for better browser compatibility
        let mimeType = 'audio/webm;codecs=opus';
        if (!MediaRecorder.isTypeSupported(mimeType)) {
            mimeType = 'audio/webm';
        }
        if (!MediaRecorder.isTypeSupported(mimeType)) {
            mimeType = 'audio/mp4';
        }
        if (!MediaRecorder.isTypeSupported(mimeType)) {
            mimeType = 'audio/ogg;codecs=opus';
        }
        if (!MediaRecorder.isTypeSupported(mimeType)) {
            mimeType = 'audio/wav';
        }
        
        console.log('Using MIME type for recording:', mimeType);
        
        // Create MediaRecorder from the destination stream
        mediaRecorder = new MediaRecorder(audioDestination.stream, {
            mimeType: mimeType
        });
        
        audioChunks = [];
        isRecording = true;
        recordingStartTime = Date.now();
        
        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };
        
        mediaRecorder.onstop = () => {
            if (audioChunks.length > 0) {
                const audioBlob = new Blob(audioChunks, { type: mimeType });
                
                // Store recording duration
                const recordingDuration = (Date.now() - recordingStartTime) / 1000; // in seconds
                sessionStorage.setItem('recordingDuration', recordingDuration.toString());
                
                // Convert blob to base64 for storage
                const reader = new FileReader();
                reader.onload = () => {
                    const base64Data = reader.result as string;
                    sessionStorage.setItem('hasRecording', 'true');
                    sessionStorage.setItem('conversationRecording', base64Data);
                    console.log('Audio recording saved to sessionStorage, duration:', recordingDuration);
                };
                reader.readAsDataURL(audioBlob);
            }
            
            // Clean up
            if (audioSource) {
                audioSource.disconnect();
                audioSource = null;
            }
            if (audioDestination) {
                audioDestination.disconnect();
                audioDestination = null;
            }
            if (userStream) {
                userStream.getTracks().forEach(track => track.stop());
            }
        };
        
        mediaRecorder.start(1000); // Collect data every second
        console.log('Audio recording started - will capture both user and AI audio');
        
    } catch (error) {
        console.error('Error starting audio recording:', error);
        alert('Could not access microphone for recording. Please allow microphone access and try again.');
    }
}

// Stop audio recording and wait for processing to complete
async function stopAudioRecording(): Promise<void> {
    return new Promise((resolve, reject) => {
        if (!mediaRecorder || !isRecording) {
            resolve();
            return;
        }
        
        isRecording = false;
        
        // Set up a timeout in case the onstop callback never fires
        const timeout = setTimeout(() => {
            console.error('Audio recording stop timeout - forcing cleanup');
            cleanupAudioRecording();
            reject(new Error('Audio recording stop timeout'));
        }, 10000); // 10 second timeout
        
        // Override the onstop callback to ensure proper sequencing
        mediaRecorder.onstop = () => {
            clearTimeout(timeout);
            
            if (audioChunks.length > 0) {
                const audioBlob = new Blob(audioChunks, { type: mediaRecorder?.mimeType || 'audio/webm' });
                
                // Store recording duration
                const recordingDuration = (Date.now() - recordingStartTime) / 1000; // in seconds
                sessionStorage.setItem('recordingDuration', recordingDuration.toString());
                
                // Convert blob to base64 for storage
                const reader = new FileReader();
                reader.onload = () => {
                    const base64Data = reader.result as string;
                    const timestamp = Date.now().toString();
                    sessionStorage.setItem('hasRecording', 'true');
                    sessionStorage.setItem('conversationRecording', base64Data);
                    sessionStorage.setItem('recordingTimestamp', timestamp);
                    console.log('✅ Audio recording processed and saved to sessionStorage, duration:', recordingDuration, 'timestamp:', timestamp);
                    
                    // Clean up and resolve
                    cleanupAudioRecording();
                    resolve();
                };
                reader.onerror = () => {
                    console.error('Error reading audio blob');
                    cleanupAudioRecording();
                    reject(new Error('Failed to process audio recording'));
                };
                reader.readAsDataURL(audioBlob);
            } else {
                console.warn('No audio chunks available');
                cleanupAudioRecording();
                resolve();
            }
        };
        
        // Stop the recording
        try {
            mediaRecorder.stop();
            console.log('Audio recording stop initiated');
        } catch (error) {
            clearTimeout(timeout);
            console.error('Error stopping media recorder:', error);
            cleanupAudioRecording();
            reject(error);
        }
    });
}

// Helper function to clean up audio recording resources
function cleanupAudioRecording() {
    if (audioSource) {
        audioSource.disconnect();
        audioSource = null;
    }
    if (audioDestination) {
        audioDestination.disconnect();
        audioDestination = null;
    }
    if (recordingStream) {
        recordingStream.getTracks().forEach(track => track.stop());
        recordingStream = null;
    }
    mediaRecorder = null;
    audioChunks = [];
}

// Save conversation and navigate to success page
async function navigateToAnalysis() {
    try {
        console.log('=== Step 1: Verifying audio recording is complete ===');
        
        // Wait a moment to ensure audio processing is complete
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Verify that we have fresh audio recording
        const hasRecording = sessionStorage.getItem('hasRecording');
        const recordedAudio = sessionStorage.getItem('conversationRecording');
        const recordingDuration = sessionStorage.getItem('recordingDuration');
        const recordingTimestamp = sessionStorage.getItem('recordingTimestamp');
        
        console.log('Audio verification - hasRecording:', hasRecording);
        console.log('Audio verification - recordedAudio exists:', !!recordedAudio);
        console.log('Audio verification - recordingDuration:', recordingDuration);
        console.log('Audio verification - recordingTimestamp:', recordingTimestamp);
        
        if (!hasRecording || hasRecording !== 'true' || !recordedAudio) {
            console.warn('⚠️ No fresh audio recording found, waiting for processing...');
            // Wait a bit more and check again
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            const retryHasRecording = sessionStorage.getItem('hasRecording');
            const retryRecordedAudio = sessionStorage.getItem('conversationRecording');
            
            if (!retryHasRecording || retryHasRecording !== 'true' || !retryRecordedAudio) {
                console.error('❌ Still no audio recording after retry - proceeding with placeholder');
            } else {
                console.log('✅ Audio recording found after retry');
            }
        } else {
            console.log('✅ Fresh audio recording verified');
        }
        
        console.log('=== Step 2: Saving conversation to database ===');
        
        // Store transcript in sessionStorage
        sessionStorage.setItem('chatTranscript', JSON.stringify(transcriptHistory));
        
        // Get the selected agent ID from localStorage
        const selectedAgentId = localStorage.getItem('selectedAgentId');
        const selectedAgentType = localStorage.getItem('selectedAgentType');
        const selectedAgentTitle = localStorage.getItem('selectedAgentTitle');
        
        // Save conversation to database with verified audio data
        const conversationData = {
            title: `${selectedAgentTitle}`,
            agent_id: selectedAgentId,
            duration_seconds: getCallDuration(),
            total_exchanges: transcriptHistory.length,
            full_conversation: getConversationHistory(),
            transcript: transcriptHistory,
            audio_data: getBase64Audio(),
            audio_format: "pcm_f32le",
            sample_rate: 44100,
            audio_duration_seconds: getAudioDuration(),
            user_agent: navigator.userAgent,
            ip_address: await getClientIP(),
            status: "completed",
            tags: ["sales_call", "training", selectedAgentType || "general"],
            notes: `Sales training conversation using ${selectedAgentTitle || 'general'} agent `
        };

        console.log('Sending conversation data to database...');
        const conversationResponse = await authenticatedFetch('/api/db/save_conversation', {
            method: 'POST',
            body: JSON.stringify(conversationData)
        });

        console.log('Conversation save response status:', conversationResponse.status);

        if (!conversationResponse.ok) {
            const errorText = await conversationResponse.text();
            console.error('Conversation save error:', errorText);
            throw new Error(`Failed to save conversation: ${conversationResponse.status} - ${errorText}`);
        }

        const conversationResult = await conversationResponse.json();
        console.log('Conversation save result:', conversationResult);
        
        if (!conversationResult.success) {
            throw new Error(`Failed to save conversation: ${conversationResult.error}`);
        }

        const conversationId = conversationResult.conversation_id;
        sessionStorage.setItem('conversationId', conversationId);
        console.log('✅ Step 2 Complete: Conversation saved successfully:', conversationId);
        
        // Add delay to ensure database write is complete
        console.log('Waiting 2 seconds for database write to complete...');
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        console.log('=== Step 3: Navigating to success page for analysis ===');
        // Navigate to success page
        window.location.href = '/success.html';
        
    } catch (error) {
        console.error('Error saving conversation:', error);
        alert('Failed to save conversation. Please try again.');
        // Don't navigate if save fails - let user try again
    }
}

// Function to generate a unique session ID
function generateSessionId(): string {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Function to clear conversation history on the backend
async function clearConversationHistory() {
    try {
        const sessionId = localStorage.getItem('currentSessionId');
        if (sessionId) {
            await fetch('/clear_conversation_history', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: sessionId })
            });
            console.log('✅ Conversation history cleared on backend');
        }
    } catch (error) {
        console.error('❌ Failed to clear conversation history:', error);
    }
}

// Function to clear previous analysis data when starting a new conversation
async function clearPreviousAnalysisData() {
    console.log('🧹 Clearing previous analysis data for fresh conversation...');
    
    // Clear conversation history on backend first
    await clearConversationHistory();
    
    // Clear analysis-related data from sessionStorage
    const keysToClear = [
        'analysisData',
        'currentAnalysisData', 
        'analysisId',
        'conversationId',
        'chatTranscript',
        'conversationRecording',
        'recordingDuration',
        'hasRecording',
        'recordingTimestamp',
        'callStartTime'
    ];
    
    keysToClear.forEach(key => {
        if (sessionStorage.getItem(key)) {
            sessionStorage.removeItem(key);
            console.log(`Cleared: ${key}`);
        }
    });
    
    // Also clear any in-memory recording state
    if (audioChunks.length > 0) {
        audioChunks = [];
        console.log('Cleared: audioChunks array');
    }
    
    // Generate a new session ID for this conversation
    const newSessionId = generateSessionId();
    localStorage.setItem('currentSessionId', newSessionId);
    
    console.log('✅ Previous analysis data cleared and new session started:', newSessionId);
}

// Helper functions for conversation data
function getCallDuration(): number {
    const startTime = sessionStorage.getItem('callStartTime');
    if (!startTime) return 0;
    const start = new Date(startTime).getTime();
    const end = new Date().getTime();
    return Math.floor((end - start) / 1000);
}

function getConversationHistory(): any[] {
    return transcriptHistory.map((item, index) => ({
        user: item.sender === 'You' ? item.text : '',
        assistant: item.sender === 'AI' ? item.text : '',
        timestamp: new Date().toISOString()
    }));
}

function getBase64Audio(): string {
    // Get actual recorded audio from sessionStorage
    const recordedAudio = sessionStorage.getItem('conversationRecording');
    const hasRecording = sessionStorage.getItem('hasRecording');
    const recordingDuration = sessionStorage.getItem('recordingDuration');
    const recordingTimestamp = sessionStorage.getItem('recordingTimestamp');
    
    console.log('getBase64Audio - hasRecording:', hasRecording);
    console.log('getBase64Audio - recordedAudio exists:', !!recordedAudio);
    console.log('getBase64Audio - recordingDuration:', recordingDuration);
    console.log('getBase64Audio - recordingTimestamp:', recordingTimestamp);
    
    if (recordedAudio && hasRecording === 'true' && recordingDuration && recordingTimestamp) {
        // Verify the audio data is substantial (not just a placeholder)
        if (recordedAudio.length > 1000 && !recordedAudio.includes('audio_data_placeholder')) {
            // Check if the recording is recent (within last 5 minutes)
            const timestamp = parseInt(recordingTimestamp);
            const now = Date.now();
            const isRecent = (now - timestamp) < 5 * 60 * 1000; // 5 minutes
            
            if (isRecent) {
                console.log('✅ Returning actual recorded audio data (length:', recordedAudio.length, ', recent:', isRecent, ')');
                return recordedAudio;
            } else {
                console.warn('⚠️ Audio recording is too old (timestamp:', timestamp, 'now:', now, ')');
            }
        } else {
            console.warn('⚠️ Audio data appears to be placeholder or too small');
        }
    }
    
    // Fallback to placeholder if no recording exists
    console.log('❌ No valid recorded audio found, using placeholder');
    return btoa('audio_data_placeholder');
}

function getAudioDuration(): number {
    // Get actual recording duration from sessionStorage
    const recordedDuration = sessionStorage.getItem('recordingDuration');
    const hasRecording = sessionStorage.getItem('hasRecording');
    const recordedAudio = sessionStorage.getItem('conversationRecording');
    
    console.log('getAudioDuration - hasRecording:', hasRecording);
    console.log('getAudioDuration - recordedDuration:', recordedDuration);
    console.log('getAudioDuration - recordedAudio exists:', !!recordedAudio);
    
    if (recordedDuration && hasRecording === 'true' && recordedAudio) {
        const duration = parseFloat(recordedDuration);
        // Verify the duration is reasonable (between 1 second and 2 hours)
        if (duration > 0 && duration < 7200) {
            console.log('✅ Using actual recording duration:', duration);
            return duration;
        } else {
            console.warn('⚠️ Recording duration seems invalid:', duration);
        }
    }
    
    // Fallback to call duration if no recording duration exists
    const callDuration = getCallDuration();
    console.log('❌ No valid recording duration found, using call duration:', callDuration);
    return callDuration;
}

async function getClientIP(): Promise<string> {
    try {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        return data.ip;
    } catch (error) {
        console.error('Error getting client IP:', error);
        return '127.0.0.1';
    }
}

async function refreshAccessToken(): Promise<string | null> {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
        console.error('No refresh token found');
        return null;
    }
    
    try {
        const response = await fetch('/auth/refresh', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                refresh_token: refreshToken
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('accessToken', data.access_token);
            localStorage.setItem('refreshToken', data.refresh_token);
            localStorage.setItem('tokenExpiresAt', data.expires_at);
            console.log('Token refreshed successfully');
            return data.access_token;
        } else {
            console.error('Failed to refresh token');
            return null;
        }
    } catch (error) {
        console.error('Error refreshing token:', error);
        return null;
    }
}

function isTokenExpired(): boolean {
    const expiresAt = localStorage.getItem('tokenExpiresAt');
    if (!expiresAt) return true;
    
    const expirationTime = new Date(expiresAt).getTime();
    const currentTime = new Date().getTime();
    
    // Consider token expired if it expires within the next 5 minutes
    return currentTime >= (expirationTime - 5 * 60 * 1000);
}

async function getAccessToken(): Promise<string> {
    // Check if token is expired
    if (isTokenExpired()) {
        console.log('Token is expired, attempting to refresh...');
        const newToken = await refreshAccessToken();
        if (!newToken) {
            console.error('Failed to refresh token, redirecting to login');
            localStorage.clear();
            window.location.href = '/login.html';
            return '';
        }
        return newToken;
    }
    
    // Check both possible key names for the access token
    const token = localStorage.getItem('accessToken');
    if (!token) {
        console.error('No access token found! User must be logged in.');
        console.log('Available localStorage keys:', Object.keys(localStorage));
        // Redirect to login if no token
        window.location.href = '/login.html';
        return '';
    }
    console.log('Found access token:', token.substring(0, 20) + '...');
    return token;
}

// Utility function for making authenticated API calls with automatic token refresh
async function authenticatedFetch(url: string, options: RequestInit = {}): Promise<Response> {
    const accessToken = await getAccessToken();
    
    const response = await fetch(url, {
        ...options,
        headers: {
            ...options.headers,
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
        }
    });
    
    // If we get a 401, try to refresh the token and retry once
    if (response.status === 401) {
        console.log('Received 401, attempting token refresh...');
        const newToken = await refreshAccessToken();
        if (newToken) {
            console.log('Token refreshed, retrying request...');
            return fetch(url, {
                ...options,
                headers: {
                    ...options.headers,
                    'Authorization': `Bearer ${newToken}`,
                    'Content-Type': 'application/json',
                }
            });
        } else {
            // Refresh failed, redirect to login
            localStorage.clear();
            window.location.href = '/login.html';
            throw new Error('Authentication failed');
        }
    }
    
    return response;
}

// Calculate confidence score based on conversation quality
function calculateConfidence(transcript: { sender: 'AI' | 'You', text: string, time: string }[]): number {
    if (transcript.length === 0) return 0;
    
    let score = 0;
    let totalExchanges = transcript.length;
    
    // Base score for having a conversation
    score += 20;
    
    // Points for each exchange (up to 50 points)
    score += Math.min(totalExchanges * 2, 50);
    
    // Points for longer responses (indicates engagement)
    const userResponses = transcript.filter(t => t.sender === 'You');
    const avgResponseLength = userResponses.reduce((sum, t) => sum + t.text.length, 0) / userResponses.length || 0;
    
    if (avgResponseLength > 50) score += 15;
    else if (avgResponseLength > 20) score += 10;
    else if (avgResponseLength > 10) score += 5;
    
    // Points for conversation flow (AI responses after user responses)
    let flowScore = 0;
    for (let i = 1; i < transcript.length; i++) {
        if (transcript[i-1].sender === 'You' && transcript[i].sender === 'AI') {
            flowScore += 2;
        }
    }
    score += Math.min(flowScore, 15);
    
    return Math.min(score, 100);
}

let isChatActive = false;
const micIcon = '<span class="material-icons" style="font-size:1.3em;color:#fff;">mic</span>';
const micOffIcon = '<span class="material-icons" style="font-size:1.3em;color:#fff;">mic_off</span>';

micBtn.onclick = async () => {
    if (!isChatActive) {
        // Clear any previous analysis data to ensure fresh analysis for new conversation
        await clearPreviousAnalysisData();
        
        // Start chat
        resetTranscript();
        startTimer();
        setVoiceWaveActive(true); // Activate voice wave animation
        
        // Start audio recording
        startAudioRecording();
        
        const welcome ="Hey, who's this?"
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
        
        // Stop audio recording only when user clicks mic_off
        if (isRecording) {
            console.log('User stopped conversation, stopping audio recording');
            try {
                await stopAudioRecording();
                console.log('✅ Audio recording stopped and processed successfully');
            } catch (error) {
                console.error('❌ Error stopping audio recording:', error);
                // Continue anyway, but log the error
            }
        }
        
        micBtn.innerHTML = micIcon;
        micBtn.style.background = 'rgba(37,99,235,0.95)';
        isChatActive = false;
        
        // Save conversation first, then navigate after successful save
        if (transcriptHistory.length > 0) {
            console.log('User ended call, saving conversation...');
            
            // Show loading state
            micBtn.innerHTML = '<span class="material-icons" style="font-size:1.3em;color:#fff;">hourglass_empty</span>';
            micBtn.style.background = 'rgba(107,114,128,0.95)';
            micBtn.disabled = true;
            
            // Save conversation and navigate
            navigateToAnalysis();
        } else {
            console.log('No transcript history, navigating directly');
            window.location.href = '/success.html';
        }
    }
};

// Initial state
micBtn.innerHTML = micIcon;
micBtn.style.background = 'rgba(37,99,235,0.95)';
isChatActive = false;
setRecordingIndicator(false);

// Set up periodic check for AI speaking status (no longer stops recording)
setInterval(() => {
    if (!isBuffering && audioPlaybackQueue.length === 0 && !isPlayingQueue) {
        // Double-check that we're not in the middle of processing
        if (!isProcessing) {
            console.log('Periodic check: AI finished speaking, recording continues');
        }
    }
}, 3000); // Check every 3 seconds

// Add user interaction handler to resume AudioContext
document.addEventListener('click', async () => {
    if (audioContext && audioContext.state === 'suspended') {
        try {
            await audioContext.resume();
            console.log('AudioContext resumed on user interaction');
        } catch (error) {
            console.error('Failed to resume AudioContext:', error);
        }
    }
}, { once: true }); 