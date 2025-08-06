(function(){const n=document.createElement("link").relList;if(n&&n.supports&&n.supports("modulepreload"))return;for(const o of document.querySelectorAll('link[rel="modulepreload"]'))i(o);new MutationObserver(o=>{for(const r of o)if(r.type==="childList")for(const a of r.addedNodes)a.tagName==="LINK"&&a.rel==="modulepreload"&&i(a)}).observe(document,{childList:!0,subtree:!0});function e(o){const r={};return o.integrity&&(r.integrity=o.integrity),o.referrerPolicy&&(r.referrerPolicy=o.referrerPolicy),o.crossOrigin==="use-credentials"?r.credentials="include":o.crossOrigin==="anonymous"?r.credentials="omit":r.credentials="same-origin",r}function i(o){if(o.ep)return;o.ep=!0;const r=e(o);fetch(o.href,r)}})();function X(){document.body.style.background="linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%)",document.body.style.fontFamily="'Inter', 'Segoe UI', Arial, sans-serif",document.body.style.margin="0",document.body.style.padding="0",document.body.style.minHeight="100vh",document.body.style.overflow="hidden";const t=document.createElement("div");t.className="top-bar",t.style.position="fixed",t.style.top="0",t.style.left="0",t.style.width="100vw",t.style.height="60px",t.style.display="flex",t.style.alignItems="center",t.style.justifyContent="center",t.style.gap="15px",t.style.padding="0 18px",t.style.background="rgba(255,255,255,0.25)",t.style.backdropFilter="blur(12px)",t.style.zIndex="100",t.style.boxShadow="0 2px 16px rgba(44,62,80,0.07)",t.style.overflow="visible";const n=document.createElement("div");n.textContent="Import/Export Analytics Consultant",n.style.fontSize="18px",n.style.fontWeight="500",n.style.letterSpacing="0.5px",n.style.color="#23272f",n.style.opacity="0.92",n.style.whiteSpace="nowrap";const e=document.createElement("div");e.style.display="flex",e.style.alignItems="center",e.style.gap="8px",e.style.fontSize="1.1rem",e.style.color="#23272f",e.style.fontWeight="500",e.style.opacity="0.85",e.style.whiteSpace="nowrap";const i=document.createElement("span");i.id="timer",i.textContent="00:00";const o=document.createElement("span");o.id="recordingDot",o.textContent="•",o.style.fontSize="1.5em",o.style.color="#e11d48",o.style.opacity="0",o.style.transition="opacity 0.3s",e.appendChild(i),e.appendChild(o),t.appendChild(n),t.appendChild(e),document.body.appendChild(t);const r=document.createElement("div");r.className="voice-wave-area",r.id="voiceWaveArea",r.style.position="fixed",r.style.top="60px",r.style.left="0",r.style.width="100vw",r.style.height="calc(100vh - 60px)",r.style.display="flex",r.style.flexDirection="column",r.style.justifyContent="center",r.style.alignItems="center",r.style.zIndex="1",r.style.background="transparent";const a=document.createElement("div");a.className="voice-wave-container",a.id="voiceWaveContainer",a.style.display="flex",a.style.alignItems="center",a.style.justifyContent="center",a.style.gap="4px",a.style.height="60px";for(let p=0;p<20;p++){const f=document.createElement("div");f.className="voice-wave-bar",f.style.width="3px",f.style.height="4px",f.style.background="rgba(37,99,235,0.3)",f.style.borderRadius="2px",f.style.transition="height 0.1s ease",a.appendChild(f)}r.appendChild(a),document.body.appendChild(r);const d=document.createElement("div");d.id="hiddenTranscript",d.style.display="none",document.body.appendChild(d);const s=document.createElement("div");s.className="mic-wrap",s.style.position="fixed",s.style.left="50%",s.style.bottom="48px",s.style.transform="translateX(-50%)",s.style.zIndex="20",s.style.display="flex",s.style.flexDirection="row",s.style.alignItems="center",s.style.gap="24px";const u=document.createElement("div");u.className="ocean-animation",u.style.position="absolute",u.style.left="50%",u.style.top="50%",u.style.transform="translate(-50%, -50%)",u.style.zIndex="-1",u.style.pointerEvents="none",u.style.width="160px",u.style.height="160px";const c=document.createElement("button");c.className="voice-btn mic-btn",c.id="micBtn",c.innerHTML='<span class="material-icons" style="font-size:20px;color:#fff;">mic</span>',c.style.width="50px",c.style.height="50px",c.style.borderRadius="50%",c.style.background="rgba(37,99,235,0.95)",c.style.color="#fff",c.style.border="none",c.style.boxShadow="0 8px 32px rgba(37,99,235,0.18), 0 2px 8px rgba(44,62,80,0.08)",c.style.display="flex",c.style.alignItems="center",c.style.justifyContent="center",c.style.fontWeight="700",c.style.fontSize="1.3rem",c.style.cursor="pointer",c.style.transition="background 0.2s, box-shadow 0.2s, transform 0.2s",c.style.position="relative",c.style.outline="none",c.style.visibility="visible",s.appendChild(c),s.appendChild(u),document.body.appendChild(s);const A=document.createElement("link");A.rel="stylesheet",A.href="https://fonts.googleapis.com/icon?family=Material+Icons",document.head.appendChild(A);const v=document.createElement("style");v.textContent=`
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
    `,document.head.appendChild(v);function w(p){if(u.innerHTML="",p)for(let f=0;f<2;f++){const h=document.createElement("div");h.className="wave"+(f===1?" wave2":""),h.style.width="0px",h.style.height="0px",h.style.background="radial-gradient(circle, #a8edea 0%, #2563eb 100%)",h.style.position="absolute",h.style.left="50%",h.style.top="50%",h.style.transform="translate(-50%, -50%)",u.appendChild(h)}}window.showOceanAnimation=w}X();let l=null,I=!1,b=!1,D=null,R=0,U=[],k=!1,y=null,S=[],C=!1,m=null,O=[],T=!1,L="",B=null,N=[],P=!1,_=0,x=null,M=null;const E=document.getElementById("micBtn"),q=document.getElementById("timer"),Z=document.getElementById("voiceWaveContainer"),F=document.getElementById("hiddenTranscript");let g="";function $(t){const n=Math.floor(t/60).toString().padStart(2,"0"),e=(t%60).toString().padStart(2,"0");return`${n}:${e}`}function ee(){R=0,q.textContent=$(R),D=window.setInterval(()=>{R++,q.textContent=$(R)},1e3)}function te(){D&&(clearInterval(D),D=null)}function z(t,n){const e=$(R);U.push({sender:t,text:n,time:e});const i=document.createElement("div");i.className="transcript-item "+(t==="AI"?"ai":"you"),i.innerHTML=`
        <div class="transcript-avatar">${t==="AI"?"🤖":"🧑"}</div>
        <div class="transcript-content">${n}</div>
        <div class="transcript-meta">${t}  ${e}</div>
    `,F.appendChild(i)}function ne(){U=[],F.innerHTML=""}function oe(){if(I||b||k)return;const t=window.SpeechRecognition||window.webkitSpeechRecognition;if(!t){alert("Your browser does not support Web Speech API.");return}l=new t,l.lang="en-US",l.interimResults=!0,l.maxAlternatives=1,l.continuous=!0,"webkitSpeechRecognition"in window&&(l.continuous=!0,l.interimResults=!0,l.maxAlternatives=1),I=!0,b=!1;let n="";g="";let e=null,i=null;l.onresult=o=>{ie(),re();let r="",a=!1;for(let d=o.resultIndex;d<o.results.length;d++){const s=o.results[d][0].transcript;o.results[d].isFinal?(n+=s,g+=s,a=!0):r+=s}if(r&&!a){e||(e=G("You"));const d=(g+" "+r).trim();e.update(d),H(!0),i&&(clearTimeout(i),i=null)}a&&n.trim()&&(i=window.setTimeout(()=>{if(n.trim().length>0){const d=n.trim();if(n="",d.length>0){Q(d),g="";const s=document.querySelector(".transcript-item.you .transcript-content");s&&(s.textContent="")}}i=null},1e3))},l.onerror=o=>{I=!1,b=!1,k=!1,l==null||l.stop(),alert("Speech recognition error: "+o.error)},l.onstart=()=>{k=!0},l.onend=()=>{if(k=!1,I&&!b&&!k&&I){const o=e?e.getText():"",r=n,a=g;setTimeout(()=>{I&&!k&&(l==null||l.start(),o&&e&&setTimeout(()=>{e&&e.update(o)},50),r&&(n=r),a&&(g=a))},50)}},l.start()}function ie(){if(window.speechSynthesis&&window.speechSynthesis.cancel(),m){try{m.stop(),m.disconnect()}catch{console.log("Audio source already stopped")}m=null}S=[],C=!1,console.log("Audio playback cleared")}function re(){console.log("User interrupted AI, continuing recording")}function ae(){if(window.speechSynthesis&&window.speechSynthesis.cancel(),m){try{m.stop(),m.disconnect()}catch{console.log("Audio source already stopped")}m=null}S=[],C=!1,O=[],T=!1,console.log("All outstanding audio cleared")}function se(){if(console.log("Stopping listening..."),I=!1,b=!1,k=!1,l)try{l.stop()}catch(e){console.log("Error stopping recognition:",e)}let t="";if(g.trim()||L.trim()){const e=[];g&&g.trim()&&e.push(g.trim()),L&&L.trim()&&e.push(L.trim());const i=document.querySelector(".transcript-item.you .transcript-content");if(i&&i.textContent&&i.textContent.trim()){const o=i.textContent.trim();o.length>0&&e.push(o)}e.length>0&&(t=e.filter((r,a)=>e.indexOf(r)===a).join(" ").replace(/\s+/g," ").trim(),console.log("Processing complete speech on stop:",t),t.length>0&&Q(t))}L="",g="";const n=document.querySelector(".transcript-item.you .transcript-content");n&&(n.textContent=""),console.log("Listening stopped")}async function Y(t){try{const n=await fetch("/tts",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text:t})});if(!n.ok)throw new Error(`HTTP ${n.status}: ${n.statusText}`);const e=await n.json();await ce(e.audio_data,"pcm_f32le",e.sample_rate)}catch(n){if(console.error("Cartesia TTS error:",n),window.speechSynthesis){const e=new SpeechSynthesisUtterance(t);e.rate=.9,e.pitch=1,P&&console.log("Using browser speech synthesis - audio will be captured via microphone"),window.speechSynthesis.speak(e)}}}async function ce(t,n="pcm_f32le",e=44100){const i=Uint8Array.from(atob(t),o=>o.charCodeAt(0));await V(i.buffer,e)}async function V(t,n){if(y||(y=new(window.AudioContext||window.webkitAudioContext)),y.state==="suspended")try{await y.resume()}catch(e){console.error("Failed to resume audio context:",e);return}try{const e=y.createBuffer(1,t.byteLength/4,n),i=e.getChannelData(0),o=new Float32Array(t);i.set(o),m&&(m.stop(),m.disconnect()),m=y.createBufferSource(),m.buffer=e,m.connect(y.destination),x&&P&&m.connect(x),m.start(),console.log("Raw PCM audio playback started successfully")}catch(e){console.error("Error playing raw PCM audio:",e)}}function Q(t){if(b)return;b=!0,z("You",t);const n=G("AI");let e="",i="";fe(t,o=>{if(e+=o,n.update(e),i+=o,le(i)){const r=J(i);r.length>0&&(O.push(...r),i="",T||j())}}).then(()=>{if(i.trim()){const o=J(i.trim());O.push(...o),T||j()}e.trim()&&z("AI",e.trim()),b=!1}).catch(o=>{n.update("Error: "+o.message),b=!1})}function le(t){return!!(/[.!?]\s*$/.test(t)||/, \s*$/.test(t)||t.length>150)}function J(t){const n=t.trim();if(!n)return[];if(/[.!?]\s*$/.test(n))return[n];if(/, \s*$/.test(n))return[n];if(n.length>150){const e=n.match(/.*[.!?]\s*$/);if(e)return[e[0].trim()]}return[]}async function de(){if(!(S.length===0||C)){for(C=!0;S.length>0;){const t=S.shift();try{await V(t,44100),m&&await new Promise(n=>{m.onended=()=>n()})}catch(n){console.error("Error playing audio from queue:",n)}}C=!1,setTimeout(()=>{ue()},500)}}async function j(){if(!T){for(T=!0;O.length>0;){const t=O.splice(0,2);for(let n=0;n<t.length;n++){const e=t[n];try{const i=await pe(e);S.push(i),C||de()}catch(i){console.error("Cartesia TTS error:",i);try{await Y(e)}catch(o){console.error("Fallback TTS error:",o)}}}}T=!1}}function ue(){!T&&S.length===0&&!C&&console.log("AI finished speaking, recording continues")}async function pe(t){return new Promise((n,e)=>{fetch("/tts_stream",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text:t})}).then(i=>{var u;if(!i.ok)throw new Error(`HTTP ${i.status}: ${i.statusText}`);const o=(u=i.body)==null?void 0:u.getReader(),r=new TextDecoder("utf-8");let a="",d=[];async function s(){try{const{done:c,value:A}=await o.read();if(c){if(d.length>0){const w=new Uint8Array(d.reduce((f,h)=>f+h.length,0));let p=0;for(const f of d)w.set(f,p),p+=f.length;n(w.buffer)}else e(new Error("No audio data received"));return}a+=r.decode(A,{stream:!0});let v=a.split(/\r?\n/);a=v.pop()||"";for(const w of v)if(w.startsWith("data: "))try{const p=JSON.parse(w.slice(6));if(p.audio_chunk){const f=Uint8Array.from(atob(p.audio_chunk),h=>h.charCodeAt(0));d.push(f)}else p.status==="complete"||p.error&&e(new Error(p.error))}catch{}s()}catch(c){e(c)}}s()}).catch(e)})}function G(t){const n=$(R),e=document.createElement("div");e.className="transcript-item "+(t==="AI"?"ai":"you"),e.innerHTML=`
        <div class="transcript-avatar">${t==="AI"?"🤖":"🧑"}</div>
        <div class="transcript-content"></div>
        <div class="transcript-meta">${t}  ${n}</div>
    `;const i=e.querySelector(".transcript-content");return F.appendChild(e),{update:o=>{i.textContent=o},remove:()=>{i.textContent=""},getText:()=>i.textContent||""}}function fe(t,n){return new Promise((e,i)=>{const o=new AbortController;fetch("/chat_stream",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:t}),signal:o.signal}).then(r=>{if(!r.body)throw new Error("No response body");const a=r.body.getReader(),d=new TextDecoder("utf-8");let s="";function u(){a.read().then(({done:c,value:A})=>{if(c){e();return}s+=d.decode(A,{stream:!0});let v=s.split(/\r?\n/);s=v.pop()||"";for(const w of v)if(w.startsWith("data: "))try{const p=JSON.parse(w.slice(6));p.reply&&n(p.reply)}catch{}u()}).catch(i)}u()}).catch(i)})}function me(t){const n=document.getElementById("recordingDot");n&&n.classList.remove("active"),window.showOceanAnimation&&window.showOceanAnimation(t)}function H(t){Z.querySelectorAll(".voice-wave-bar").forEach(e=>{t?e.classList.add("active"):e.classList.remove("active")})}async function ye(){try{const t=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:!0,noiseSuppression:!0,autoGainControl:!0,sampleRate:44100}});y||(y=new(window.AudioContext||window.webkitAudioContext)),x=y.createMediaStreamDestination(),M=y.createMediaStreamSource(t),M.connect(x);let n="audio/webm;codecs=opus";MediaRecorder.isTypeSupported(n)||(n="audio/webm"),MediaRecorder.isTypeSupported(n)||(n="audio/mp4"),MediaRecorder.isTypeSupported(n)||(n="audio/ogg;codecs=opus"),MediaRecorder.isTypeSupported(n)||(n="audio/wav"),console.log("Using MIME type for recording:",n),B=new MediaRecorder(x.stream,{mimeType:n}),N=[],P=!0,_=Date.now(),B.ondataavailable=e=>{e.data.size>0&&N.push(e.data)},B.onstop=()=>{if(N.length>0){const e=new Blob(N,{type:n}),i=(Date.now()-_)/1e3;sessionStorage.setItem("recordingDuration",i.toString());const o=new FileReader;o.onload=()=>{const r=o.result;sessionStorage.setItem("hasRecording","true"),sessionStorage.setItem("conversationRecording",r),console.log("Audio recording saved to sessionStorage, duration:",i)},o.readAsDataURL(e)}M&&(M.disconnect(),M=null),x&&(x.disconnect(),x=null),t&&t.getTracks().forEach(e=>e.stop())},B.start(1e3),console.log("Audio recording started - will capture both user and AI audio")}catch(t){console.error("Error starting audio recording:",t),alert("Could not access microphone for recording. Please allow microphone access and try again.")}}function he(){B&&P&&(P=!1,B.stop(),console.log("Audio recording stopped"))}function ge(){sessionStorage.setItem("chatTranscript",JSON.stringify(U)),window.location.href="/success.html"}let W=!1;const K='<span class="material-icons" style="font-size:1.3em;color:#fff;">mic</span>',we='<span class="material-icons" style="font-size:1.3em;color:#fff;">mic_off</span>';E.onclick=()=>{if(W)ae(),se(),te(),H(!1),P&&(console.log("User stopped conversation, stopping audio recording"),he()),E.innerHTML=K,E.style.background="rgba(37,99,235,0.95)",W=!1,setTimeout(()=>{U.length>0&&ge()},500);else{ne(),ee(),H(!0),ye();const t="Hey, who's this?";z("AI",t),Y(t),oe(),E.innerHTML=we,E.style.background="rgba(229,39,76,0.92)",W=!0}};E.innerHTML=K;E.style.background="rgba(37,99,235,0.95)";W=!1;me(!1);setInterval(()=>{!T&&S.length===0&&!C&&(b||console.log("Periodic check: AI finished speaking, recording continues"))},3e3);document.addEventListener("click",async()=>{if(y&&y.state==="suspended")try{await y.resume(),console.log("AudioContext resumed on user interaction")}catch(t){console.error("Failed to resume AudioContext:",t)}},{once:!0});
