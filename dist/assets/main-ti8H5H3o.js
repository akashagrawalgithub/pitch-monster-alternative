(function(){const e=document.createElement("link").relList;if(e&&e.supports&&e.supports("modulepreload"))return;for(const o of document.querySelectorAll('link[rel="modulepreload"]'))i(o);new MutationObserver(o=>{for(const a of o)if(a.type==="childList")for(const l of a.addedNodes)l.tagName==="LINK"&&l.rel==="modulepreload"&&i(l)}).observe(document,{childList:!0,subtree:!0});function n(o){const a={};return o.integrity&&(a.integrity=o.integrity),o.referrerPolicy&&(a.referrerPolicy=o.referrerPolicy),o.crossOrigin==="use-credentials"?a.credentials="include":o.crossOrigin==="anonymous"?a.credentials="omit":a.credentials="same-origin",a}function i(o){if(o.ep)return;o.ep=!0;const a=n(o);fetch(o.href,a)}})();function te(){return sessionStorage.getItem("authenticated")==="true"?!0:(window.location.href="/login.html",!1)}function ne(){document.body.style.background="linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%)",document.body.style.fontFamily="'Inter', 'Segoe UI', Arial, sans-serif",document.body.style.margin="0",document.body.style.padding="0",document.body.style.minHeight="100vh",document.body.style.overflow="hidden";const t=document.createElement("div");t.className="top-bar",t.style.position="fixed",t.style.top="0",t.style.left="0",t.style.width="100vw",t.style.height="60px",t.style.display="flex",t.style.alignItems="center",t.style.justifyContent="center",t.style.gap="15px",t.style.padding="0 18px",t.style.background="rgba(255,255,255,0.25)",t.style.backdropFilter="blur(12px)",t.style.zIndex="100",t.style.boxShadow="0 2px 16px rgba(44,62,80,0.07)",t.style.overflow="visible";const e=document.createElement("button");e.innerHTML="← Back to Agents",e.style.position="absolute",e.style.left="18px",e.style.background="rgba(255,255,255,0.8)",e.style.border="1px solid rgba(0,0,0,0.1)",e.style.borderRadius="8px",e.style.padding="8px 16px",e.style.fontSize="14px",e.style.fontWeight="500",e.style.color="#374151",e.style.cursor="pointer",e.style.transition="all 0.2s",e.onclick=()=>window.location.href="/agents.html",e.onmouseover=()=>{e.style.background="rgba(255,255,255,0.95)",e.style.transform="translateY(-1px)"},e.onmouseout=()=>{e.style.background="rgba(255,255,255,0.8)",e.style.transform="translateY(0)"};const n=localStorage.getItem("selectedAgentType")||"payment-followup",i={"payment-followup":"Payment Follow-up Training","competitor-objection":"Competitor Objection Training","lead-to-demo":"Lead to Demo Training","closing-skills":"Closing Skills Training","cold-calling":"Cold Calling Training","discovery-call":"Discovery Call Training"},o=document.createElement("div");o.textContent=i[n]||"Sales Training",o.style.fontSize="18px",o.style.fontWeight="500",o.style.letterSpacing="0.5px",o.style.color="#23272f",o.style.opacity="0.92",o.style.whiteSpace="nowrap";const a=document.createElement("div");a.style.display="flex",a.style.alignItems="center",a.style.gap="8px",a.style.fontSize="1.1rem",a.style.color="#23272f",a.style.fontWeight="500",a.style.opacity="0.85",a.style.whiteSpace="nowrap";const l=document.createElement("span");l.id="timer",l.textContent="00:00";const c=document.createElement("span");c.id="recordingDot",c.textContent="•",c.style.fontSize="1.5em",c.style.color="#e11d48",c.style.opacity="0",c.style.transition="opacity 0.3s",a.appendChild(l),a.appendChild(c),t.appendChild(e),t.appendChild(o),t.appendChild(a),document.body.appendChild(t);const s=document.createElement("div");s.className="voice-wave-area",s.id="voiceWaveArea",s.style.position="fixed",s.style.top="60px",s.style.left="0",s.style.width="100vw",s.style.height="calc(100vh - 60px)",s.style.display="flex",s.style.flexDirection="column",s.style.justifyContent="center",s.style.alignItems="center",s.style.zIndex="1",s.style.background="transparent";const y=document.createElement("div");y.className="voice-wave-container",y.id="voiceWaveContainer",y.style.display="flex",y.style.alignItems="center",y.style.justifyContent="center",y.style.gap="4px",y.style.height="60px";for(let W=0;W<20;W++){const g=document.createElement("div");g.className="voice-wave-bar",g.style.width="3px",g.style.height="4px",g.style.background="rgba(37,99,235,0.3)",g.style.borderRadius="2px",g.style.transition="height 0.1s ease",y.appendChild(g)}s.appendChild(y),document.body.appendChild(s);const v=document.createElement("div");v.id="hiddenTranscript",v.style.display="none",document.body.appendChild(v);const f=document.createElement("div");f.className="mic-wrap",f.style.position="fixed",f.style.left="50%",f.style.bottom="48px",f.style.transform="translateX(-50%)",f.style.zIndex="20",f.style.display="flex",f.style.flexDirection="row",f.style.alignItems="center",f.style.gap="24px";const u=document.createElement("div");u.className="ocean-animation",u.style.position="absolute",u.style.left="50%",u.style.top="50%",u.style.transform="translate(-50%, -50%)",u.style.zIndex="-1",u.style.pointerEvents="none",u.style.width="160px",u.style.height="160px";const r=document.createElement("button");r.className="voice-btn mic-btn",r.id="micBtn",r.innerHTML='<span class="material-icons" style="font-size:20px;color:#fff;">mic</span>',r.style.width="50px",r.style.height="50px",r.style.borderRadius="50%",r.style.background="rgba(37,99,235,0.95)",r.style.color="#fff",r.style.border="none",r.style.boxShadow="0 8px 32px rgba(37,99,235,0.18), 0 2px 8px rgba(44,62,80,0.08)",r.style.display="flex",r.style.alignItems="center",r.style.justifyContent="center",r.style.fontWeight="700",r.style.fontSize="1.3rem",r.style.cursor="pointer",r.style.transition="background 0.2s, box-shadow 0.2s, transform 0.2s",r.style.position="relative",r.style.outline="none",r.style.visibility="visible",f.appendChild(r),f.appendChild(u),document.body.appendChild(f);const m=document.createElement("link");m.rel="stylesheet",m.href="https://fonts.googleapis.com/icon?family=Material+Icons",document.head.appendChild(m);const x=document.createElement("style");x.textContent=`
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
    `,document.head.appendChild(x);function M(W){if(u.innerHTML="",W)for(let g=0;g<2;g++){const S=document.createElement("div");S.className="wave"+(g===1?" wave2":""),S.style.width="0px",S.style.height="0px",S.style.background="radial-gradient(circle, #a8edea 0%, #2563eb 100%)",S.style.position="absolute",S.style.left="50%",S.style.top="50%",S.style.transform="translate(-50%, -50%)",u.appendChild(S)}}window.showOceanAnimation=M}te()?ne():window.location.href="/login.html";let d=null,I=!1,b=!1,U=null,R=0,F=[],E=!1,h=null,C=[],A=!1,p=null,D=[],k=!1,O="",P=null,$=[],L=!1,Y=0,T=null,N=null;const B=document.getElementById("micBtn"),J=document.getElementById("timer"),oe=document.getElementById("voiceWaveContainer"),j=document.getElementById("hiddenTranscript");let w="";function H(t){const e=Math.floor(t/60).toString().padStart(2,"0"),n=(t%60).toString().padStart(2,"0");return`${e}:${n}`}function ie(){R=0,J.textContent=H(R),U=window.setInterval(()=>{R++,J.textContent=H(R)},1e3)}function ae(){U&&(clearInterval(U),U=null)}function _(t,e){const n=H(R);F.push({sender:t,text:e,time:n});const i=document.createElement("div");i.className="transcript-item "+(t==="AI"?"ai":"you"),i.innerHTML=`
        <div class="transcript-avatar">${t==="AI"?"🤖":"🧑"}</div>
        <div class="transcript-content">${e}</div>
        <div class="transcript-meta">${t}  ${n}</div>
    `,j.appendChild(i)}function re(){F=[],j.innerHTML=""}function se(){if(I||b||E)return;const t=window.SpeechRecognition||window.webkitSpeechRecognition;if(!t){alert("Your browser does not support Web Speech API.");return}d=new t,d.lang="en-US",d.interimResults=!0,d.maxAlternatives=1,d.continuous=!0,"webkitSpeechRecognition"in window&&(d.continuous=!0,d.interimResults=!0,d.maxAlternatives=1),I=!0,b=!1;let e="";w="";let n=null,i=null;d.onresult=o=>{ce(),le();let a="",l=!1;for(let c=o.resultIndex;c<o.results.length;c++){const s=o.results[c][0].transcript;o.results[c].isFinal?(e+=s,w+=s,l=!0):a+=s}if(a&&!l){n||(n=Z("You"));const c=(w+" "+a).trim();n.update(c),q(!0),i&&(clearTimeout(i),i=null)}l&&e.trim()&&(i=window.setTimeout(()=>{if(e.trim().length>0){const c=e.trim();if(e="",c.length>0){X(c),w="";const s=document.querySelector(".transcript-item.you .transcript-content");s&&(s.textContent="")}}i=null},1e3))},d.onerror=o=>{I=!1,b=!1,E=!1,d==null||d.stop(),alert("Speech recognition error: "+o.error)},d.onstart=()=>{E=!0},d.onend=()=>{if(E=!1,I&&!b&&!E&&I){const o=n?n.getText():"",a=e,l=w;setTimeout(()=>{I&&!E&&(d==null||d.start(),o&&n&&setTimeout(()=>{n&&n.update(o)},50),a&&(e=a),l&&(w=l))},50)}},d.start()}function ce(){if(window.speechSynthesis&&window.speechSynthesis.cancel(),p){try{p.stop(),p.disconnect()}catch{console.log("Audio source already stopped")}p=null}C=[],A=!1,console.log("Audio playback cleared")}function le(){console.log("User interrupted AI, continuing recording")}function de(){if(window.speechSynthesis&&window.speechSynthesis.cancel(),p){try{p.stop(),p.disconnect()}catch{console.log("Audio source already stopped")}p=null}C=[],A=!1,D=[],k=!1,console.log("All outstanding audio cleared")}function ue(){if(console.log("Stopping listening..."),I=!1,b=!1,E=!1,d)try{d.stop()}catch(n){console.log("Error stopping recognition:",n)}let t="";if(w.trim()||O.trim()){const n=[];w&&w.trim()&&n.push(w.trim()),O&&O.trim()&&n.push(O.trim());const i=document.querySelector(".transcript-item.you .transcript-content");if(i&&i.textContent&&i.textContent.trim()){const o=i.textContent.trim();o.length>0&&n.push(o)}n.length>0&&(t=n.filter((a,l)=>n.indexOf(a)===l).join(" ").replace(/\s+/g," ").trim(),console.log("Processing complete speech on stop:",t),t.length>0&&X(t))}O="",w="";const e=document.querySelector(".transcript-item.you .transcript-content");e&&(e.textContent=""),console.log("Listening stopped")}async function G(t){try{const e=await fetch("/tts",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text:t})});if(!e.ok)throw new Error(`HTTP ${e.status}: ${e.statusText}`);const n=await e.json();await pe(n.audio_data,"pcm_f32le",n.sample_rate)}catch(e){if(console.error("Cartesia TTS error:",e),window.speechSynthesis){const n=new SpeechSynthesisUtterance(t);n.rate=.9,n.pitch=1,L&&console.log("Using browser speech synthesis - audio will be captured via microphone"),window.speechSynthesis.speak(n)}}}async function pe(t,e="pcm_f32le",n=44100){const i=Uint8Array.from(atob(t),o=>o.charCodeAt(0));await K(i.buffer,n)}async function K(t,e){if(h||(h=new(window.AudioContext||window.webkitAudioContext)),h.state==="suspended")try{await h.resume()}catch(n){console.error("Failed to resume audio context:",n);return}try{const n=h.createBuffer(1,t.byteLength/4,e),i=n.getChannelData(0),o=new Float32Array(t);i.set(o),p&&(p.stop(),p.disconnect()),p=h.createBufferSource(),p.buffer=n,p.connect(h.destination),T&&L&&p.connect(T),p.start(),console.log("Raw PCM audio playback started successfully")}catch(n){console.error("Error playing raw PCM audio:",n)}}function X(t){if(b)return;b=!0,_("You",t);const e=Z("AI");let n="",i="";ge(t,o=>{if(n+=o,e.update(n),i+=o,fe(i)){const a=V(i);a.length>0&&(D.push(...a),i="",k||Q())}}).then(()=>{if(i.trim()){const o=V(i.trim());D.push(...o),k||Q()}n.trim()&&_("AI",n.trim()),b=!1}).catch(o=>{e.update("Error: "+o.message),b=!1})}function fe(t){return!!(/[.!?]\s*$/.test(t)||/, \s*$/.test(t)||t.length>150)}function V(t){const e=t.trim();if(!e)return[];if(/[.!?]\s*$/.test(e))return[e];if(/, \s*$/.test(e))return[e];if(e.length>150){const n=e.match(/.*[.!?]\s*$/);if(n)return[n[0].trim()]}return[]}async function me(){if(!(C.length===0||A)){for(A=!0;C.length>0;){const t=C.shift();try{await K(t,44100),p&&await new Promise(e=>{p.onended=()=>e()})}catch(e){console.error("Error playing audio from queue:",e)}}A=!1,setTimeout(()=>{ye()},500)}}async function Q(){if(!k){for(k=!0;D.length>0;){const t=D.splice(0,2);for(let e=0;e<t.length;e++){const n=t[e];try{const i=await he(n);C.push(i),A||me()}catch(i){console.error("Cartesia TTS error:",i);try{await G(n)}catch(o){console.error("Fallback TTS error:",o)}}}}k=!1}}function ye(){!k&&C.length===0&&!A&&console.log("AI finished speaking, recording continues")}async function he(t){return new Promise((e,n)=>{fetch("/tts_stream",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text:t})}).then(i=>{var y;if(!i.ok)throw new Error(`HTTP ${i.status}: ${i.statusText}`);const o=(y=i.body)==null?void 0:y.getReader(),a=new TextDecoder("utf-8");let l="",c=[];async function s(){try{const{done:v,value:f}=await o.read();if(v){if(c.length>0){const r=new Uint8Array(c.reduce((x,M)=>x+M.length,0));let m=0;for(const x of c)r.set(x,m),m+=x.length;e(r.buffer)}else n(new Error("No audio data received"));return}l+=a.decode(f,{stream:!0});let u=l.split(/\r?\n/);l=u.pop()||"";for(const r of u)if(r.startsWith("data: "))try{const m=JSON.parse(r.slice(6));if(m.audio_chunk){const x=Uint8Array.from(atob(m.audio_chunk),M=>M.charCodeAt(0));c.push(x)}else m.status==="complete"||m.error&&n(new Error(m.error))}catch{}s()}catch(v){n(v)}}s()}).catch(n)})}function Z(t){const e=H(R),n=document.createElement("div");n.className="transcript-item "+(t==="AI"?"ai":"you"),n.innerHTML=`
        <div class="transcript-avatar">${t==="AI"?"🤖":"🧑"}</div>
        <div class="transcript-content"></div>
        <div class="transcript-meta">${t}  ${e}</div>
    `;const i=n.querySelector(".transcript-content");return j.appendChild(n),{update:o=>{i.textContent=o},remove:()=>{i.textContent=""},getText:()=>i.textContent||""}}function ge(t,e){return new Promise((n,i)=>{const o=new AbortController;fetch("/chat_stream",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:t}),signal:o.signal}).then(a=>{if(!a.body)throw new Error("No response body");const l=a.body.getReader(),c=new TextDecoder("utf-8");let s="";function y(){l.read().then(({done:v,value:f})=>{if(v){n();return}s+=c.decode(f,{stream:!0});let u=s.split(/\r?\n/);s=u.pop()||"";for(const r of u)if(r.startsWith("data: "))try{const m=JSON.parse(r.slice(6));m.reply&&e(m.reply)}catch{}y()}).catch(i)}y()}).catch(i)})}function we(t){const e=document.getElementById("recordingDot");e&&e.classList.remove("active"),window.showOceanAnimation&&window.showOceanAnimation(t)}function q(t){oe.querySelectorAll(".voice-wave-bar").forEach(n=>{t?n.classList.add("active"):n.classList.remove("active")})}async function be(){try{const t=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:!0,noiseSuppression:!0,autoGainControl:!0,sampleRate:44100}});h||(h=new(window.AudioContext||window.webkitAudioContext)),T=h.createMediaStreamDestination(),N=h.createMediaStreamSource(t),N.connect(T);let e="audio/webm;codecs=opus";MediaRecorder.isTypeSupported(e)||(e="audio/webm"),MediaRecorder.isTypeSupported(e)||(e="audio/mp4"),MediaRecorder.isTypeSupported(e)||(e="audio/ogg;codecs=opus"),MediaRecorder.isTypeSupported(e)||(e="audio/wav"),console.log("Using MIME type for recording:",e),P=new MediaRecorder(T.stream,{mimeType:e}),$=[],L=!0,Y=Date.now(),P.ondataavailable=n=>{n.data.size>0&&$.push(n.data)},P.onstop=()=>{if($.length>0){const n=new Blob($,{type:e}),i=(Date.now()-Y)/1e3;sessionStorage.setItem("recordingDuration",i.toString());const o=new FileReader;o.onload=()=>{const a=o.result;sessionStorage.setItem("hasRecording","true"),sessionStorage.setItem("conversationRecording",a),console.log("Audio recording saved to sessionStorage, duration:",i)},o.readAsDataURL(n)}N&&(N.disconnect(),N=null),T&&(T.disconnect(),T=null),t&&t.getTracks().forEach(n=>n.stop())},P.start(1e3),console.log("Audio recording started - will capture both user and AI audio")}catch(t){console.error("Error starting audio recording:",t),alert("Could not access microphone for recording. Please allow microphone access and try again.")}}function ve(){P&&L&&(L=!1,P.stop(),console.log("Audio recording stopped"))}function xe(){sessionStorage.setItem("chatTranscript",JSON.stringify(F)),window.location.href="/success.html"}let z=!1;const ee='<span class="material-icons" style="font-size:1.3em;color:#fff;">mic</span>',Se='<span class="material-icons" style="font-size:1.3em;color:#fff;">mic_off</span>';B.onclick=()=>{if(z)de(),ue(),ae(),q(!1),L&&(console.log("User stopped conversation, stopping audio recording"),ve()),B.innerHTML=ee,B.style.background="rgba(37,99,235,0.95)",z=!1,setTimeout(()=>{F.length>0&&xe()},500);else{re(),ie(),q(!0),be();const t="Hey, who's this?";_("AI",t),G(t),se(),B.innerHTML=Se,B.style.background="rgba(229,39,76,0.92)",z=!0}};B.innerHTML=ee;B.style.background="rgba(37,99,235,0.95)";z=!1;we(!1);setInterval(()=>{!k&&C.length===0&&!A&&(b||console.log("Periodic check: AI finished speaking, recording continues"))},3e3);document.addEventListener("click",async()=>{if(h&&h.state==="suspended")try{await h.resume(),console.log("AudioContext resumed on user interaction")}catch(t){console.error("Failed to resume AudioContext:",t)}},{once:!0});
