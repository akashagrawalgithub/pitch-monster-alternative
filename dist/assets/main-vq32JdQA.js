(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const o of document.querySelectorAll('link[rel="modulepreload"]'))i(o);new MutationObserver(o=>{for(const a of o)if(a.type==="childList")for(const l of a.addedNodes)l.tagName==="LINK"&&l.rel==="modulepreload"&&i(l)}).observe(document,{childList:!0,subtree:!0});function n(o){const a={};return o.integrity&&(a.integrity=o.integrity),o.referrerPolicy&&(a.referrerPolicy=o.referrerPolicy),o.crossOrigin==="use-credentials"?a.credentials="include":o.crossOrigin==="anonymous"?a.credentials="omit":a.credentials="same-origin",a}function i(o){if(o.ep)return;o.ep=!0;const a=n(o);fetch(o.href,a)}})();function ne(){return localStorage.getItem("authenticated")==="true"?!0:(window.location.href="/login.html",!1)}function oe(){document.body.style.background="linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%)",document.body.style.fontFamily="'Inter', 'Segoe UI', Arial, sans-serif",document.body.style.margin="0",document.body.style.padding="0",document.body.style.minHeight="100vh",document.body.style.overflow="hidden";const e=document.createElement("div");e.className="top-bar",e.style.position="fixed",e.style.top="0",e.style.left="0",e.style.width="100vw",e.style.height="60px",e.style.display="flex",e.style.alignItems="center",e.style.justifyContent="center",e.style.gap="15px",e.style.padding="0 18px",e.style.background="rgba(255,255,255,0.25)",e.style.backdropFilter="blur(12px)",e.style.zIndex="100",e.style.boxShadow="0 2px 16px rgba(44,62,80,0.07)",e.style.overflow="visible";const t=document.createElement("button");t.innerHTML="← Back to Agents",t.style.position="absolute",t.style.left="18px",t.style.background="rgba(255,255,255,0.8)",t.style.border="1px solid rgba(0,0,0,0.1)",t.style.borderRadius="8px",t.style.padding="8px 16px",t.style.fontSize="14px",t.style.fontWeight="500",t.style.color="#374151",t.style.cursor="pointer",t.style.transition="all 0.2s",t.onclick=()=>window.location.href="/agents.html",t.onmouseover=()=>{t.style.background="rgba(255,255,255,0.95)",t.style.transform="translateY(-1px)"},t.onmouseout=()=>{t.style.background="rgba(255,255,255,0.8)",t.style.transform="translateY(0)"};const n=localStorage.getItem("selectedAgentType")||"payment-followup",i={"payment-followup":"Payment Follow-up Training","competitor-objection":"Competitor Objection Training","lead-to-demo":"Lead to Demo Training","closing-skills":"Closing Skills Training","cold-calling":"Cold Calling Training","discovery-call":"Discovery Call Training"},o=document.createElement("div");o.textContent=i[n]||"Sales Training",o.style.fontSize="18px",o.style.fontWeight="500",o.style.letterSpacing="0.5px",o.style.color="#23272f",o.style.opacity="0.92",o.style.whiteSpace="nowrap";const a=document.createElement("div");a.style.display="flex",a.style.alignItems="center",a.style.gap="8px",a.style.fontSize="1.1rem",a.style.color="#23272f",a.style.fontWeight="500",a.style.opacity="0.85",a.style.whiteSpace="nowrap";const l=document.createElement("span");l.id="timer",l.textContent="00:00";const c=document.createElement("span");c.id="recordingDot",c.textContent="•",c.style.fontSize="1.5em",c.style.color="#e11d48",c.style.opacity="0",c.style.transition="opacity 0.3s",a.appendChild(l),a.appendChild(c),e.appendChild(t),e.appendChild(o),e.appendChild(a),document.body.appendChild(e);const r=document.createElement("div");r.className="voice-wave-area",r.id="voiceWaveArea",r.style.position="fixed",r.style.top="60px",r.style.left="0",r.style.width="100vw",r.style.height="calc(100vh - 60px)",r.style.display="flex",r.style.flexDirection="column",r.style.justifyContent="center",r.style.alignItems="center",r.style.zIndex="1",r.style.background="transparent";const y=document.createElement("div");y.className="voice-wave-container",y.id="voiceWaveContainer",y.style.display="flex",y.style.alignItems="center",y.style.justifyContent="center",y.style.gap="4px",y.style.height="60px";for(let $=0;$<20;$++){const h=document.createElement("div");h.className="voice-wave-bar",h.style.width="3px",h.style.height="4px",h.style.background="rgba(37,99,235,0.3)",h.style.borderRadius="2px",h.style.transition="height 0.1s ease",y.appendChild(h)}r.appendChild(y),document.body.appendChild(r);const x=document.createElement("div");x.id="hiddenTranscript",x.style.display="none",document.body.appendChild(x);const f=document.createElement("div");f.className="mic-wrap",f.style.position="fixed",f.style.left="50%",f.style.bottom="48px",f.style.transform="translateX(-50%)",f.style.zIndex="20",f.style.display="flex",f.style.flexDirection="row",f.style.alignItems="center",f.style.gap="24px";const u=document.createElement("div");u.className="ocean-animation",u.style.position="absolute",u.style.left="50%",u.style.top="50%",u.style.transform="translate(-50%, -50%)",u.style.zIndex="-1",u.style.pointerEvents="none",u.style.width="160px",u.style.height="160px";const s=document.createElement("button");s.className="voice-btn mic-btn",s.id="micBtn",s.innerHTML='<span class="material-icons" style="font-size:20px;color:#fff;">mic</span>',s.style.width="50px",s.style.height="50px",s.style.borderRadius="50%",s.style.background="rgba(37,99,235,0.95)",s.style.color="#fff",s.style.border="none",s.style.boxShadow="0 8px 32px rgba(37,99,235,0.18), 0 2px 8px rgba(44,62,80,0.08)",s.style.display="flex",s.style.alignItems="center",s.style.justifyContent="center",s.style.fontWeight="700",s.style.fontSize="1.3rem",s.style.cursor="pointer",s.style.transition="background 0.2s, box-shadow 0.2s, transform 0.2s",s.style.position="relative",s.style.outline="none",s.style.visibility="visible",f.appendChild(s),f.appendChild(u),document.body.appendChild(f);const m=document.createElement("link");m.rel="stylesheet",m.href="https://fonts.googleapis.com/icon?family=Material+Icons",document.head.appendChild(m);const S=document.createElement("style");S.textContent=`
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
    `,document.head.appendChild(S);function L($){if(u.innerHTML="",$)for(let h=0;h<2;h++){const T=document.createElement("div");T.className="wave"+(h===1?" wave2":""),T.style.width="0px",T.style.height="0px",T.style.background="radial-gradient(circle, #a8edea 0%, #2563eb 100%)",T.style.position="absolute",T.style.left="50%",T.style.top="50%",T.style.transform="translate(-50%, -50%)",u.appendChild(T)}}window.showOceanAnimation=L}ne()?oe():window.location.href="/login.html";let d=null,E=!1,b=!1,U=null,R=0,P=[],B=!1,g=null,A=[],k=!1,p=null,N=[],I=!1,_="",D=null,W=[],O=!1,Y=0,C=null,M=null;const v=document.getElementById("micBtn"),J=document.getElementById("timer"),ie=document.getElementById("voiceWaveContainer"),q=document.getElementById("hiddenTranscript");let w="";function z(e){const t=Math.floor(e/60).toString().padStart(2,"0"),n=(e%60).toString().padStart(2,"0");return`${t}:${n}`}function ae(){R=0,sessionStorage.setItem("callStartTime",new Date().toISOString()),J.textContent=z(R),U=window.setInterval(()=>{R++,J.textContent=z(R)},1e3)}function se(){U&&(clearInterval(U),U=null)}function H(e,t){const n=z(R);P.push({sender:e,text:t,time:n});const i=document.createElement("div");i.className="transcript-item "+(e==="AI"?"ai":"you"),i.innerHTML=`
        <div class="transcript-avatar">${e==="AI"?"🤖":"🧑"}</div>
        <div class="transcript-content">${t}</div>
        <div class="transcript-meta">${e}  ${n}</div>
    `,q.appendChild(i)}function re(){P=[],q.innerHTML=""}function ce(){if(E||b||B)return;const e=window.SpeechRecognition||window.webkitSpeechRecognition;if(!e){alert("Your browser does not support Web Speech API.");return}d=new e,d.lang="en-US",d.interimResults=!0,d.maxAlternatives=1,d.continuous=!0,"webkitSpeechRecognition"in window&&(d.continuous=!0,d.interimResults=!0,d.maxAlternatives=1),E=!0,b=!1;let t="";w="";let n=null,i=null;d.onresult=o=>{le(),de();let a="",l=!1;for(let c=o.resultIndex;c<o.results.length;c++){const r=o.results[c][0].transcript;o.results[c].isFinal?(t+=r,w+=r,l=!0):a+=r}if(a&&!l){n||(n=Z("You"));const c=(w+" "+a).trim();n.update(c),j(!0),i&&(clearTimeout(i),i=null)}l&&t.trim()&&(i=window.setTimeout(()=>{if(t.trim().length>0){const c=t.trim();if(t="",c.length>0){X(c),w="";const r=document.querySelector(".transcript-item.you .transcript-content");r&&(r.textContent="")}}i=null},1e3))},d.onerror=o=>{E=!1,b=!1,B=!1,d==null||d.stop(),alert("Speech recognition error: "+o.error)},d.onstart=()=>{B=!0},d.onend=()=>{if(B=!1,E&&!b&&!B&&E){const o=n?n.getText():"",a=t,l=w;setTimeout(()=>{E&&!B&&(d==null||d.start(),o&&n&&setTimeout(()=>{n&&n.update(o)},50),a&&(t=a),l&&(w=l))},50)}},d.start()}function le(){if(window.speechSynthesis&&window.speechSynthesis.cancel(),p){try{p.stop(),p.disconnect()}catch{console.log("Audio source already stopped")}p=null}A=[],k=!1,console.log("Audio playback cleared")}function de(){console.log("User interrupted AI, continuing recording")}function ue(){if(window.speechSynthesis&&window.speechSynthesis.cancel(),p){try{p.stop(),p.disconnect()}catch{console.log("Audio source already stopped")}p=null}A=[],k=!1,N=[],I=!1,console.log("All outstanding audio cleared")}function pe(){if(console.log("Stopping listening..."),E=!1,b=!1,B=!1,d)try{d.stop()}catch(n){console.log("Error stopping recognition:",n)}let e="";if(w.trim()||_.trim()){const n=[];w&&w.trim()&&n.push(w.trim()),_&&_.trim()&&n.push(_.trim());const i=document.querySelector(".transcript-item.you .transcript-content");if(i&&i.textContent&&i.textContent.trim()){const o=i.textContent.trim();o.length>0&&n.push(o)}n.length>0&&(e=n.filter((a,l)=>n.indexOf(a)===l).join(" ").replace(/\s+/g," ").trim(),console.log("Processing complete speech on stop:",e),e.length>0&&X(e))}_="",w="";const t=document.querySelector(".transcript-item.you .transcript-content");t&&(t.textContent=""),console.log("Listening stopped")}async function G(e){try{const t=await fetch("/tts",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text:e})});if(!t.ok)throw new Error(`HTTP ${t.status}: ${t.statusText}`);const n=await t.json();await fe(n.audio_data,"pcm_f32le",n.sample_rate)}catch(t){if(console.error("Cartesia TTS error:",t),window.speechSynthesis){const n=new SpeechSynthesisUtterance(e);n.rate=.9,n.pitch=1,O&&console.log("Using browser speech synthesis - audio will be captured via microphone"),window.speechSynthesis.speak(n)}}}async function fe(e,t="pcm_f32le",n=44100){const i=Uint8Array.from(atob(e),o=>o.charCodeAt(0));await K(i.buffer,n)}async function K(e,t){if(g||(g=new(window.AudioContext||window.webkitAudioContext)),g.state==="suspended")try{await g.resume()}catch(n){console.error("Failed to resume audio context:",n);return}try{const n=g.createBuffer(1,e.byteLength/4,t),i=n.getChannelData(0),o=new Float32Array(e);i.set(o),p&&(p.stop(),p.disconnect()),p=g.createBufferSource(),p.buffer=n,p.connect(g.destination),C&&O&&p.connect(C),p.start(),console.log("Raw PCM audio playback started successfully")}catch(n){console.error("Error playing raw PCM audio:",n)}}function X(e){if(b)return;b=!0,H("You",e);const t=Z("AI");let n="",i="";we(e,o=>{if(n+=o,t.update(n),i+=o,me(i)){const a=V(i);a.length>0&&(N.push(...a),i="",I||Q())}}).then(()=>{if(i.trim()){const o=V(i.trim());N.push(...o),I||Q()}n.trim()&&H("AI",n.trim()),b=!1}).catch(o=>{t.update("Error: "+o.message),b=!1})}function me(e){return!!(/[.!?]\s*$/.test(e)||/, \s*$/.test(e)||e.length>150)}function V(e){const t=e.trim();if(!t)return[];if(/[.!?]\s*$/.test(t))return[t];if(/, \s*$/.test(t))return[t];if(t.length>150){const n=t.match(/.*[.!?]\s*$/);if(n)return[n[0].trim()]}return[]}async function ye(){if(!(A.length===0||k)){for(k=!0;A.length>0;){const e=A.shift();try{await K(e,44100),p&&await new Promise(t=>{p.onended=()=>t()})}catch(t){console.error("Error playing audio from queue:",t)}}k=!1,setTimeout(()=>{ge()},500)}}async function Q(){if(!I){for(I=!0;N.length>0;){const e=N.splice(0,2);for(let t=0;t<e.length;t++){const n=e[t];try{const i=await he(n);A.push(i),k||ye()}catch(i){console.error("Cartesia TTS error:",i);try{await G(n)}catch(o){console.error("Fallback TTS error:",o)}}}}I=!1}}function ge(){!I&&A.length===0&&!k&&console.log("AI finished speaking, recording continues")}async function he(e){return new Promise((t,n)=>{fetch("/tts_stream",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text:e})}).then(i=>{var y;if(!i.ok)throw new Error(`HTTP ${i.status}: ${i.statusText}`);const o=(y=i.body)==null?void 0:y.getReader(),a=new TextDecoder("utf-8");let l="",c=[];async function r(){try{const{done:x,value:f}=await o.read();if(x){if(c.length>0){const s=new Uint8Array(c.reduce((S,L)=>S+L.length,0));let m=0;for(const S of c)s.set(S,m),m+=S.length;t(s.buffer)}else n(new Error("No audio data received"));return}l+=a.decode(f,{stream:!0});let u=l.split(/\r?\n/);l=u.pop()||"";for(const s of u)if(s.startsWith("data: "))try{const m=JSON.parse(s.slice(6));if(m.audio_chunk){const S=Uint8Array.from(atob(m.audio_chunk),L=>L.charCodeAt(0));c.push(S)}else m.status==="complete"||m.error&&n(new Error(m.error))}catch{}r()}catch(x){n(x)}}r()}).catch(n)})}function Z(e){const t=z(R),n=document.createElement("div");n.className="transcript-item "+(e==="AI"?"ai":"you"),n.innerHTML=`
        <div class="transcript-avatar">${e==="AI"?"🤖":"🧑"}</div>
        <div class="transcript-content"></div>
        <div class="transcript-meta">${e}  ${t}</div>
    `;const i=n.querySelector(".transcript-content");return q.appendChild(n),{update:o=>{i.textContent=o},remove:()=>{i.textContent=""},getText:()=>i.textContent||""}}function we(e,t){return new Promise((n,i)=>{const o=new AbortController;fetch("/chat_stream",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:e}),signal:o.signal}).then(a=>{if(!a.body)throw new Error("No response body");const l=a.body.getReader(),c=new TextDecoder("utf-8");let r="";function y(){l.read().then(({done:x,value:f})=>{if(x){n();return}r+=c.decode(f,{stream:!0});let u=r.split(/\r?\n/);r=u.pop()||"";for(const s of u)if(s.startsWith("data: "))try{const m=JSON.parse(s.slice(6));m.reply&&t(m.reply)}catch{}y()}).catch(i)}y()}).catch(i)})}function ve(e){const t=document.getElementById("recordingDot");t&&t.classList.remove("active"),window.showOceanAnimation&&window.showOceanAnimation(e)}function j(e){ie.querySelectorAll(".voice-wave-bar").forEach(n=>{e?n.classList.add("active"):n.classList.remove("active")})}async function be(){try{const e=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:!0,noiseSuppression:!0,autoGainControl:!0,sampleRate:44100}});g||(g=new(window.AudioContext||window.webkitAudioContext)),C=g.createMediaStreamDestination(),M=g.createMediaStreamSource(e),M.connect(C);let t="audio/webm;codecs=opus";MediaRecorder.isTypeSupported(t)||(t="audio/webm"),MediaRecorder.isTypeSupported(t)||(t="audio/mp4"),MediaRecorder.isTypeSupported(t)||(t="audio/ogg;codecs=opus"),MediaRecorder.isTypeSupported(t)||(t="audio/wav"),console.log("Using MIME type for recording:",t),D=new MediaRecorder(C.stream,{mimeType:t}),W=[],O=!0,Y=Date.now(),D.ondataavailable=n=>{n.data.size>0&&W.push(n.data)},D.onstop=()=>{if(W.length>0){const n=new Blob(W,{type:t}),i=(Date.now()-Y)/1e3;sessionStorage.setItem("recordingDuration",i.toString());const o=new FileReader;o.onload=()=>{const a=o.result;sessionStorage.setItem("hasRecording","true"),sessionStorage.setItem("conversationRecording",a),console.log("Audio recording saved to sessionStorage, duration:",i)},o.readAsDataURL(n)}M&&(M.disconnect(),M=null),C&&(C.disconnect(),C=null),e&&e.getTracks().forEach(n=>n.stop())},D.start(1e3),console.log("Audio recording started - will capture both user and AI audio")}catch(e){console.error("Error starting audio recording:",e),alert("Could not access microphone for recording. Please allow microphone access and try again.")}}function xe(){D&&O&&(O=!1,D.stop(),console.log("Audio recording stopped"))}async function Se(){try{console.log("=== Step 1: Saving conversation to database ==="),sessionStorage.setItem("chatTranscript",JSON.stringify(P));const e={title:"Sales Call - "+new Date().toLocaleString(),duration_seconds:ee(),total_exchanges:P.length,full_conversation:Te(),transcript:P,audio_data:Ce(),audio_format:"pcm_f32le",sample_rate:44100,audio_duration_seconds:Ae(),user_agent:navigator.userAgent,ip_address:await ke(),status:"completed",tags:["sales_call","training"],notes:"Sales training conversation"};console.log("Sending conversation data to database...");const t=await fetch("/api/db/save_conversation",{method:"POST",headers:{"Content-Type":"application/json",Authorization:`Bearer ${Ie()}`},body:JSON.stringify(e)});if(console.log("Conversation save response status:",t.status),!t.ok){const o=await t.text();throw console.error("Conversation save error:",o),new Error(`Failed to save conversation: ${t.status} - ${o}`)}const n=await t.json();if(console.log("Conversation save result:",n),!n.success)throw new Error(`Failed to save conversation: ${n.error}`);const i=n.conversation_id;sessionStorage.setItem("conversationId",i),console.log("✅ Step 1 Complete: Conversation saved successfully:",i),console.log("Waiting 2 seconds for database write to complete..."),await new Promise(o=>setTimeout(o,2e3)),console.log("=== Step 2: Navigating to success page for analysis ==="),window.location.href="/success.html"}catch(e){console.error("Error saving conversation:",e),alert("Failed to save conversation. Please try again.")}}function ee(){const e=sessionStorage.getItem("callStartTime");if(!e)return 0;const t=new Date(e).getTime(),n=new Date().getTime();return Math.floor((n-t)/1e3)}function Te(){return P.map((e,t)=>({user:e.sender==="You"?e.text:"",assistant:e.sender==="AI"?e.text:"",timestamp:new Date().toISOString()}))}function Ce(){return btoa("audio_data_placeholder")}function Ae(){return ee()}async function ke(){try{return(await(await fetch("https://api.ipify.org?format=json")).json()).ip}catch(e){return console.error("Error getting client IP:",e),"127.0.0.1"}}function Ie(){const e=localStorage.getItem("access_token")||localStorage.getItem("accessToken");return e?(console.log("Found access token:",e.substring(0,20)+"..."),e):(console.error("No access token found! User must be logged in."),console.log("Available localStorage keys:",Object.keys(localStorage)),window.location.href="/login.html","")}let F=!1;const te='<span class="material-icons" style="font-size:1.3em;color:#fff;">mic</span>',Ee='<span class="material-icons" style="font-size:1.3em;color:#fff;">mic_off</span>';v.onclick=()=>{if(F)ue(),pe(),se(),j(!1),O&&(console.log("User stopped conversation, stopping audio recording"),xe()),v.innerHTML=te,v.style.background="rgba(37,99,235,0.95)",F=!1,P.length>0?(console.log("User ended call, saving conversation..."),v.innerHTML='<span class="material-icons" style="font-size:1.3em;color:#fff;">hourglass_empty</span>',v.style.background="rgba(107,114,128,0.95)",v.disabled=!0,Se()):(console.log("No transcript history, navigating directly"),window.location.href="/success.html");else{re(),ae(),j(!0),be();const e="Hey, who's this?";H("AI",e),G(e),ce(),v.innerHTML=Ee,v.style.background="rgba(229,39,76,0.92)",F=!0}};v.innerHTML=te;v.style.background="rgba(37,99,235,0.95)";F=!1;ve(!1);setInterval(()=>{!I&&A.length===0&&!k&&(b||console.log("Periodic check: AI finished speaking, recording continues"))},3e3);document.addEventListener("click",async()=>{if(g&&g.state==="suspended")try{await g.resume(),console.log("AudioContext resumed on user interaction")}catch(e){console.error("Failed to resume AudioContext:",e)}},{once:!0});
