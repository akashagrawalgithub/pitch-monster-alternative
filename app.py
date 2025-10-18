from flask import Flask, request, send_from_directory, jsonify, Response, stream_with_context
from flask_cors import CORS
from flask_sock import Sock
from openai import OpenAI
import os
from datetime import datetime
import time
from prompts import analysisPrompt, bestPitchPrompt
from prompt_manager import prompt_manager
# Removed unused import for performance
from cartesia import Cartesia
import base64
import numpy as np
import json
from backend_api import db_api
from supabase import create_client, Client
import websockets
import asyncio
from threading import Thread

app = Flask(__name__, template_folder='static')
sock = Sock(app)
CORS(app, origins=['http://localhost:3000', 'http://localhost:8000', 'https://pitch-monster-alternative.onrender.com'])

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
CARTESIA_API_KEY = os.environ.get("CARTESIA_API_KEY")

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")

# Initialize OpenAI client with connection pooling
import httpx
openai_client = OpenAI(
    api_key=OPENAI_API_KEY,
    http_client=httpx.Client(
        limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
        timeout=httpx.Timeout(90.0, connect=15.0),  # Increased timeout for complex requests
        http2=True
    )
)

# Initialize Cartesia client
cartesia_client = Cartesia(api_key=CARTESIA_API_KEY)

# Per-session conversation tracking - each session gets fresh history
session_conversations = {}
session_seeds = {}
current_session_id = None
current_user_id = None

# Simple response cache for common inputs (to reduce API calls)
# Removed per user request to avoid added behavior

def process_raw_audio(audio_bytes, sample_rate=44100):
    """Process raw PCM f32le audio data efficiently"""
    try:
        # Convert bytes to numpy array for efficient processing
        audio_array = np.frombuffer(audio_bytes, dtype=np.float32)
        
        # Normalize audio to prevent clipping
        if np.max(np.abs(audio_array)) > 0:
            audio_array = audio_array / np.max(np.abs(audio_array)) * 0.95
        
        # Convert back to bytes
        return audio_array.tobytes()
    except Exception as e:
        # Removed logging for performance
        return audio_bytes

def get_current_user_id():
    """Get current user ID from request headers"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        # We'll use a simple approach for now - you can integrate with your auth system
        return "user_" + str(hash(token) % 10000)  # Simple user ID generation
    except Exception as e:
        # Removed logging for performance
        return None

def generate_conversation_seed(conversation_history):
    """Ultra-lightweight: Track only questions asked to prevent repetition"""
    if not conversation_history or len(conversation_history) < 3:
        return None
    
    try:
        total = len(conversation_history)
        
        # Extract only questions (ends with ?) from all assistant messages
        questions_asked = []
        for msg in conversation_history:
            assistant_text = msg['assistant']
            # Find sentences ending with ?
            sentences = assistant_text.split('.')
            for sentence in sentences:
                if '?' in sentence:
                    # Extract just the question part
                    question = sentence.split('?')[0] + '?'
                    question = question.strip()
                    if len(question) > 10:  # Filter out too short
                        questions_asked.append(question[:80])  # Truncate long questions
        
        if not questions_asked:
            return None
        
        # Build ultra-compact seed
        seed_text = f"{total} exchanges done. Questions already asked:\n"
        seed_text += " | ".join(questions_asked)
        seed_text += "\nNEVER repeat these questions."
        
        return seed_text
    except:
        return None

import os

# Check if we're in development or production
IS_DEVELOPMENT = False  # Set to False to use built dist files

@app.route('/')
def index():
    if IS_DEVELOPMENT:
        # In development, redirect to Vite dev server
        return send_from_directory('static', 'index.html')
    else:
        # In production, serve from dist folder
        return send_from_directory('dist', 'index.html')

@app.route('/analysis.html')
def analysis():
    if IS_DEVELOPMENT:
        # In development, serve from static folder
        return send_from_directory('static', 'analysis.html')
    else:
        # In production, serve from dist folder
        return send_from_directory('dist', 'analysis.html')


@app.route('/success.html')
def success():
    if IS_DEVELOPMENT:
        # In development, serve from static folder
        return send_from_directory('static', 'success.html')
    else:
        # In production, serve from dist folder
        return send_from_directory('dist', 'success.html')

@app.route('/admin.html')
def admin():
    if IS_DEVELOPMENT:
        # In development, serve from static folder
        return send_from_directory('static', 'admin.html')
    else:
        # In production, serve from dist folder
        return send_from_directory('dist', 'admin.html')

@app.route('/user-management.html')
def user_management():
    if IS_DEVELOPMENT:
        # In development, serve from static folder
        return send_from_directory('static', 'user-management.html')
    else:
        # In production, serve from dist folder
        return send_from_directory('dist', 'user-management.html')

@app.route('/users.html')
def users():
    if IS_DEVELOPMENT:
        # In development, serve from static folder
        return send_from_directory('static', 'users.html')
    else:
        # In production, serve from dist folder
        return send_from_directory('dist', 'users.html')

@app.route('/marketing.html')
def marketing():
    if IS_DEVELOPMENT:
        # In development, serve from static folder
        return send_from_directory('static', 'marketing.html')
    else:
        # In production, serve from dist folder
        return send_from_directory('dist', 'marketing.html')

@app.route('/test_analysis.html')
def test_analysis_page():
    if IS_DEVELOPMENT:
        # In development, serve from static folder
        return send_from_directory('static', 'test_analysis.html')
    else:
        # In production, serve from dist folder
        return send_from_directory('dist', 'test_analysis.html')

@app.route('/test_redirect.html')
def test_redirect_page():
    if IS_DEVELOPMENT:
        # In development, serve from static folder
        return send_from_directory('static', 'test_redirect.html')
    else:
        # In production, serve from dist folder
        return send_from_directory('dist', 'test_redirect.html')

@app.route('/login.html')
def login_page():
    if IS_DEVELOPMENT:
        # In development, serve from static folder
        return send_from_directory('static', 'login.html')
    else:
        # In production, serve from dist folder
        return send_from_directory('dist', 'login.html')

@app.route('/agents.html')
def agents_page():
    if IS_DEVELOPMENT:
        # In development, serve from static folder
        return send_from_directory('static', 'agents.html')
    else:
        # In production, serve from dist folder
        return send_from_directory('dist', 'agents.html')

@app.route('/past-conversations.html')
def past_conversations_page():
    if IS_DEVELOPMENT:
        # In development, serve from static folder
        return send_from_directory('static', 'past-conversations.html')
    else:
        # In production, serve from dist folder
        return send_from_directory('dist', 'past-conversations.html')

@app.route('/agent-info.html')
def agent_info_page():
    if IS_DEVELOPMENT:
        # In development, serve from static folder
        return send_from_directory('static', 'agent-info.html')
    else:
        # In production, serve from dist folder
        return send_from_directory('dist', 'agent-info.html')

@sock.route('/ws/openai-realtime')
def openai_realtime_proxy(ws):
    """Secure WebSocket proxy for OpenAI Realtime API"""
    try:
        # OpenAI Realtime API WebSocket URL
        openai_ws_url = f"wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"
        
        # Headers for OpenAI connection (with API key)
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1"
        }
        
        # Create async function to handle the proxy
        async def proxy_messages():
            async with websockets.connect(openai_ws_url, extra_headers=headers) as openai_ws:
                # Create tasks for bidirectional communication
                async def forward_to_openai():
                    """Forward messages from client to OpenAI"""
                    try:
                        while True:
                            # Receive from client
                            message = ws.receive()
                            if message is None:
                                break
                            # Forward to OpenAI
                            await openai_ws.send(message)
                    except Exception as e:
                        print(f"Error forwarding to OpenAI: {e}")
                
                async def forward_to_client():
                    """Forward messages from OpenAI to client"""
                    try:
                        async for message in openai_ws:
                            # Forward to client
                            ws.send(message)
                    except Exception as e:
                        print(f"Error forwarding to client: {e}")
                
                # Run both directions concurrently
                await asyncio.gather(
                    forward_to_openai(),
                    forward_to_client(),
                    return_exceptions=True
                )
        
        # Run the async proxy in a new event loop
        asyncio.run(proxy_messages())
        
    except Exception as e:
        print(f"WebSocket proxy error: {e}")
        ws.close()

@app.route('/conversation.html')
def conversation_page():
    # Render template without API key (now using secure proxy)
    return render_template('conversation.html')

@app.route('/tts', methods=['POST'])
def text_to_speech():
    """Generate speech from text using Cartesia"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Generate audio using Cartesia with raw format for minimal latency
        response = cartesia_client.tts.bytes(
            model_id="sonic-turbo",
            transcript=text,
            voice={
                "mode": "id",
                "id": "4df027cb-2920-4a1f-8c34-f21529d5c3fe",  # Barbershop Man - good for conversations
            },
            language="en",
            output_format={
                "container": "raw",
                "sample_rate": 44100,
                "encoding": "pcm_f32le",
            },
        )
        
        # Handle generator response from Cartesia
        if hasattr(response, '__iter__'):
            # Convert generator to bytes
            audio_bytes = b''.join(response)
        else:
            audio_bytes = response
        
        # Process raw audio for better quality and efficiency
        processed_audio = process_raw_audio(audio_bytes)
        
        # Convert audio bytes to base64 for frontend
        audio_base64 = base64.b64encode(processed_audio).decode('utf-8')
        
        return jsonify({
            "audio_data": audio_base64,
            "format": "pcm_f32le",
            "sample_rate": 44100
        })
        
    except Exception as e:
        # Removed logging for performance
        return jsonify({"error": f"TTS generation failed: {str(e)}"}), 500

@app.route('/tts_stream', methods=['POST'])
def text_to_speech_stream():
    """Stream TTS audio using Cartesia websocket"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        def generate_audio_stream():
            # This is a simplified version - in production you'd use websockets
            # For now, we'll generate the full audio and stream it in chunks
            try:
                response = cartesia_client.tts.bytes(
                    model_id="sonic-turbo",
                    transcript=text,
                    voice={
                        "mode": "id",
                        "id": "4df027cb-2920-4a1f-8c34-f21529d5c3fe",
                    },
                    language="en",
                    output_format={
                        "container": "raw",
                        "sample_rate": 44100,
                        "encoding": "pcm_f32le",
                    },
                )
                
                # Handle generator response from Cartesia
                if hasattr(response, '__iter__'):
                    # Convert generator to bytes
                    audio_bytes = b''.join(response)
                else:
                    audio_bytes = response
                
                # Process raw audio for better quality and efficiency
                processed_audio = process_raw_audio(audio_bytes)
                
                # Stream audio in chunks
                chunk_size = 4096
                for i in range(0, len(processed_audio), chunk_size):
                    chunk = processed_audio[i:i + chunk_size]
                    chunk_base64 = base64.b64encode(chunk).decode('utf-8')
                    yield f"data: {{\"audio_chunk\": \"{chunk_base64}\", \"format\": \"pcm_f32le\", \"sample_rate\": 44100}}\n\n"
                
                yield f"data: {{\"status\": \"complete\"}}\n\n"
                
            except Exception as e:
                yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"
        
        return Response(stream_with_context(generate_audio_stream()), 
                       mimetype='text/event-stream')
        
    except Exception as e:
        return jsonify({"error": "TTS streaming failed"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    global session_conversations, session_seeds
    
    user_input = request.json.get('message', '').strip()
    agent_type = request.json.get('agent_type', 'discovery-call')
    session_id = request.json.get('session_id', 'default')
    
    if not user_input:
        return jsonify({"reply": "I didn't catch that. Could you repeat?"})

    # Get or create conversation history for this session
    if session_id not in session_conversations:
        session_conversations[session_id] = []
    
    conversation_history = session_conversations[session_id]
    
    # Generate/update conversation seed to maintain context beyond the truncated history
    if len(conversation_history) >= 3:
        session_seeds[session_id] = generate_conversation_seed(conversation_history)
    
    # Use up to the last 10 turns for maximum speed
    max_history = 10
    recent_history = conversation_history[-max_history:] if len(conversation_history) > max_history else conversation_history

    # Get the dynamic prompt for this agent
    dynamic_prompt = prompt_manager.get_prompt(agent_type)
    
    messages = [{
        "role": "system",
        "content": dynamic_prompt
    }]
    
    if session_seeds.get(session_id):
        messages.append({"role": "system", "content": f"IMPORTANT - DO NOT repeat earlier questions. {session_seeds[session_id]}"})

    # Add recent conversation history
    for msg in recent_history:
        messages.append({"role": "user", "content": msg["user"]})
        messages.append({"role": "assistant", "content": msg["assistant"]})

    messages.append({"role": "user", "content": user_input})

    try:
        start_time = time.time()
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=80,  # Reduced for maximum speed
            temperature=0.0,  # Zero for fastest responses
            presence_penalty=0.0,  # Zero for speed
            frequency_penalty=0.0,  # Zero for speed
            timeout=8  # 4 second hard deadline
        )
        
        reply = response.choices[0].message.content.strip()
        
        # Add to conversation history for this session
        conversation_history.append({
            "user": user_input,
            "assistant": reply,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep history manageable (max 15 messages for maximum speed)
        if len(conversation_history) > 15:
            conversation_history[:] = conversation_history[-15:]
        
        # Removed logging for performance
        
        return jsonify({"reply": reply})

    except Exception as e:
        error_message = str(e).lower()
        if "rate limit" in error_message:
            return jsonify({"reply": "Too many requests. Please wait a moment."}), 429
        elif "timeout" in error_message:
            return jsonify({"reply": "Request timed out. Please try again."}), 408
        elif "api" in error_message:
            return jsonify({"reply": "Service temporarily unavailable."}), 503
        else:
            # Removed logging for performance
            return jsonify({"reply": "Sorry, I'm having trouble. Please try again."}), 500

@app.route('/api/get_agent_prompt', methods=['GET'])
def get_agent_prompt():
    """Get the prompt for a specific agent type"""
    try:
        agent_type = request.args.get('agent_type', 'discovery-call')
        print(f"📥 Getting prompt for agent type: {agent_type}")
        prompt = prompt_manager.get_prompt(agent_type)
        print(f"✅ Prompt fetched successfully, length: {len(prompt)}")
        return jsonify({
            'success': True,
            'prompt': prompt,
            'agent_type': agent_type
        })
    except Exception as e:
        print(f"❌ Error in get_agent_prompt: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'prompt': 'You are a helpful sales training coach.'
        }), 500

@app.route('/chat_stream', methods=['POST'])
def chat_stream():
    global session_conversations, session_seeds
    
    user_input = request.json.get('message', '').strip()
    agent_type = request.json.get('agent_type', 'discovery-call')
    session_id = request.json.get('session_id', 'default')
    
    if not user_input:
        return Response('data: {"reply": "I didn\'t catch that. Could you repeat?"}\n\n', mimetype='text/event-stream')

    # Get or create conversation history for this session
    if session_id not in session_conversations:
        session_conversations[session_id] = []
    
    conversation_history = session_conversations[session_id]
    
    # Generate/update conversation seed to maintain context beyond the truncated history
    if len(conversation_history) >= 3:
        session_seeds[session_id] = generate_conversation_seed(conversation_history)
    
    max_history = 5  # Reduced for maximum speed
    recent_history = conversation_history[-max_history:] if len(conversation_history) > max_history else conversation_history

    # Get the dynamic prompt for this agent
    dynamic_prompt = prompt_manager.get_prompt(agent_type)
    
    messages = [{
        "role": "system",
        "content": dynamic_prompt
    }]
    if session_seeds.get(session_id):
        messages.append({"role": "system", "content": f"IMPORTANT - DO NOT repeat earlier questions. {session_seeds[session_id]}"})
    for msg in recent_history:
        messages.append({"role": "user", "content": msg["user"]})
        messages.append({"role": "assistant", "content": msg["assistant"]})
    messages.append({"role": "user", "content": user_input})
    
    # Debug: Log messages being sent to AI
    # print(f"🔍 Messages being sent to AI: {len(messages)} total")
    for i, msg in enumerate(messages[-6:]):  # Show last 6 messages
        print(f"🔍 Message {i}: {msg['role']}: {msg['content'][:100]}...")

    def generate():
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=80,  # Reduced for maximum speed
                temperature=0.0,  # Zero for fastest responses
                presence_penalty=0.0,  # Zero for speed
                frequency_penalty=0.0,  # Zero for speed
                stream=True,
                timeout=8  
            )
            full_reply = ""
            for chunk in response:
                delta = chunk.choices[0].delta.content
                if delta:
                    full_reply += delta
                    # Send as SSE event
                    yield f"data: {{\"reply\": \"{delta.replace('\\', '\\\\').replace('"', '\\\"')}\"}}\n\n"
            # Add to conversation history for this session after streaming is done
            conversation_history.append({
                "user": user_input,
                "assistant": full_reply,
                "timestamp": datetime.now().isoformat()
            })
            if len(conversation_history) > 15:
                conversation_history[:] = conversation_history[-15:]
            
            # Debug: Log conversation history after saving
            print(f"🔍 Conversation history saved. Length: {len(conversation_history)}")
            print(f"🔍 Last entry: User: {user_input[:50]}... | Assistant: {full_reply[:50]}...")
                
        except Exception as e:
            error_message = str(e).lower()
            if "rate limit" in error_message:
                yield 'data: {"reply": "Too many requests. Please wait a moment."}\n\n'
            elif "timeout" in error_message:
                yield 'data: {"reply": "Request timed out. Please try again."}\n\n'
            elif "api" in error_message:
                yield 'data: {"reply": "Service temporarily unavailable."}\n\n'
            else:
                # Removed logging for performance
                yield 'data: {"reply": "Sorry, I\'m having trouble. Please try again."}\n\n'

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/clear_conversation_history', methods=['POST'])
def clear_conversation_history():
    """Clear conversation history for a specific session"""
    global session_conversations, session_seeds
    
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        
        # Clear the conversation history for this session
        if session_id in session_conversations:
            session_conversations[session_id] = []
            # Removed logging for performance
        else:
            # Initialize empty history for new session
            session_conversations[session_id] = []
            # Removed logging for performance
        
        # Clear the conversation seed for this session
        if session_id in session_seeds:
            del session_seeds[session_id]
        
        return jsonify({"success": True, "message": "Conversation history cleared"})
        
    except Exception as e:
        # Removed logging for performance
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/analyze_conversation', methods=['POST'])
def analyze_conversation():
    """Analyze conversation transcript and return comprehensive feedback"""
    try:
        data = request.json
        transcript = data.get('transcript', [])
        agent_id = data.get('agent_id')
        agent_key = data.get('agent_key')
        
        if not transcript:
            return jsonify({"error": "No transcript provided"}), 400
        
        # Convert transcript to a readable format for analysis
        conversation_text = ""
        for i, exchange in enumerate(transcript, 1):
            sender = exchange.get('sender', 'Unknown')
            text = exchange.get('text', '')
            time_stamp = exchange.get('time', '')
            conversation_text += f"Exchange {i} ({time_stamp}):\n{sender}: {text}\n\n"
        
        # Fetch sample script from database if agent information is provided
        sample_script = ""
        if agent_id or agent_key:
            try:
                from database_operations import DatabaseManager
                db = DatabaseManager()
                
                if agent_key:
                    # Get agent by key
                    agent = db.get_agent_by_key(agent_key)
                    if agent:
                        sample_script = agent.get('sample_script', '')
                elif agent_id:
                    # Get agent by ID
                    agent = db.get_agent_by_id(agent_id)
                    if agent:
                        sample_script = agent.get('sample_script', '')
            except Exception as e:
                print(f"Error fetching sample script: {e}")
                # Continue without sample script if there's an error
        
        # Prepare the analysis prompt with the conversation and sample script
        analysis_prompt = analysisPrompt
        if sample_script:
            analysis_prompt += f"\n\n### SAMPLE SCRIPT FOR REFERENCE:\n\n{sample_script}"
        
        analysis_messages = [
            {
                "role": "system",
                "content": analysis_prompt
            },
            {
                "role": "user",
                "content": f"Please analyze the following sales conversation transcript and provide feedback in the specified JSON format:\n\n{conversation_text}"
            }
        ]
        
        # Call OpenAI for analysis
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Using GPT-4 for better analysis
            messages=analysis_messages,
            max_tokens=2000,
            temperature=0.1,  # Low temperature for consistent analysis
            response_format={"type": "json_object"}  # Ensure JSON response
        )
        
        analysis_result = response.choices[0].message.content.strip()
        
        # Parse the JSON response
        try:
            analysis_data = json.loads(analysis_result)
            
            # Validate required fields
            required_fields = [
                'session_info', 'overall_score', 'key_metrics', 
                'voice_delivery_analysis', 'sales_skills_assessment', 
                'sales_process_flow', 'strengths', 'improvements'
            ]
            
            for field in required_fields:
                if field not in analysis_data:
                    return jsonify({"error": f"Missing required field: {field}"}), 500
            
            return jsonify(analysis_data)
            
        except json.JSONDecodeError as e:
            # Removed logging for performance
            return jsonify({"error": "Invalid JSON response from analysis"}), 500
            
    except Exception as e:
        error_message = str(e).lower()
        if "rate limit" in error_message:
            return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
        elif "timeout" in error_message:
            return jsonify({"error": "Analysis request timed out. Please try again."}), 408
        elif "api" in error_message:
            return jsonify({"error": f"OpenAI API error: {str(e)}"}), 503
        else:
            # Removed logging for performance
            return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

@app.route('/best-pitch', methods=['POST'])
def best_pitch():
    try:
        data = request.json
        transcript = data.get('transcript', [])
        analysis_data = data.get('analysis_data', None)  # Optional: previous analysis for context
        
        if not transcript:
            return jsonify({"error": "No transcript provided"}), 400
        
        # Convert transcript to a readable format
        conversation_text = ""
        for i, exchange in enumerate(transcript, 1):
            sender = exchange.get('sender', 'Unknown')
            text = exchange.get('text', '')
            time_stamp = exchange.get('time', '')
            conversation_text += f"Exchange {i} ({time_stamp}):\n{sender}: {text}\n\n"
        
        # Add context from previous analysis if available
        context_info = ""
        if analysis_data:
            overall_score = analysis_data.get('overall_score', {}).get('percentage', 0)
            conversation_length = len(transcript)
            voice_analysis = analysis_data.get('voice_delivery_analysis', {})
            sales_skills = analysis_data.get('sales_skills_assessment', {})
            
            context_info = f"""

ANALYSIS CONTEXT FOR DYNAMIC SCORING:
- Original Overall Score: {overall_score}%
- Total Conversation Exchanges: {conversation_length}
- Voice Analysis Scores: {voice_analysis}
- Sales Skills Scores: {sales_skills}

INSTRUCTIONS:
- Use the original score ({overall_score}%) as the baseline
- Only process the {conversation_length} exchanges that actually happened
- Calculate realistic perfect score based on conversation length and complexity
- Show improvement from {overall_score}% to realistic perfect score
"""
        
        # Prepare the analysis messages
        messages = [
            {
                "role": "system", 
                "content": bestPitchPrompt
            },
            {
                "role": "user",
                "content": f"Please analyze this sales conversation and provide the perfect pitch version with dynamic scoring based on actual performance:\n\n{conversation_text}{context_info}"
            }
        ]
        
       # Call OpenAI for perfect pitch generation with optimized settings
        response = openai_client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            max_tokens=30000,
            temperature=0.1,
            response_format={"type": "json_object"},
            timeout=90.0
        )
        
        perfect_pitch_result = response.choices[0].message.content.strip()
        
        # Debug logging for JSON parsing issues
        print(f"🔍 Raw OpenAI response length: {len(perfect_pitch_result)}")
        print(f"🔍 Raw response preview: {perfect_pitch_result[:200]}...")
        
        try:
            perfect_pitch_data = json.loads(perfect_pitch_result)
            required_fields = ['perfect_conversation', 'overall_improvements', 'score_improvement']
            for field in required_fields:
                if field not in perfect_pitch_data:
                    return jsonify({"error": f"Missing required field: {field}"}), 500
            
            return jsonify(perfect_pitch_data)
            
        except json.JSONDecodeError as e:
            # Enhanced error logging for debugging
            print(f"❌ JSON Parse Error: {str(e)}")
            print(f"❌ Raw response that failed to parse: {perfect_pitch_result}")
            
            # Check if response was truncated (common cause of JSON errors)
            if not perfect_pitch_result.endswith('}'):
                print("⚠️ Response appears to be truncated - incomplete JSON")
                return jsonify({
                    "error": "Response was truncated - insufficient token limit for conversation length",
                    "debug_info": f"Response length: {len(perfect_pitch_result)}, Ends with: {perfect_pitch_result[-50:]}",
                    "suggestion": "Try with a shorter conversation or increase token limit"
                }), 500
            
            # Try to extract JSON from response if it has extra text
            try:
                # Look for JSON object in the response
                start_idx = perfect_pitch_result.find('{')
                end_idx = perfect_pitch_result.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_part = perfect_pitch_result[start_idx:end_idx]
                    print(f"🔍 Attempting to parse extracted JSON: {json_part[:200]}...")
                    perfect_pitch_data = json.loads(json_part)
                    return jsonify(perfect_pitch_data)
            except:
                pass
            
            return jsonify({
                "error": "Invalid JSON response from perfect pitch generation",
                "debug_info": f"Response length: {len(perfect_pitch_result)}, Preview: {perfect_pitch_result[:100]}"
            }), 500
            
    except Exception as e:
        # Removed logging for performance
        
        error_message = str(e).lower()
        if "rate limit" in error_message:
            return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
        elif "timeout" in error_message:
            return jsonify({"error": "Perfect pitch request timed out. Please try again."}), 408
        elif "api" in error_message or "openai" in error_message:
            return jsonify({"error": f"OpenAI API error: {str(e)}"}), 503
        else:
            # Return a more detailed error message for debugging
            return jsonify({
                "error": f"Perfect pitch generation failed: {str(e)}",
                "error_type": type(e).__name__,
                "debug_info": "Check server logs for more details"
            }), 500

# Register the database API blueprint
app.register_blueprint(db_api, url_prefix='/api/db')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

@app.route('/login', methods=['POST'])
def login():
    """UserManager email/password login"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Use our custom UserManager for authentication
        from user_manager import user_manager
        user_data = user_manager.authenticate_user(email, password)
        
        if user_data:
            return jsonify({
                'message': 'Login successful',
                'success': True,
                'user': user_data
            })
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
        
    except Exception as e:
        # Removed logging for performance
        return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/auth/check', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'authenticated': False}), 401
        
        token = auth_header.split(' ')[1]
        
        # Use our custom UserManager to verify token
        from user_manager import user_manager
        payload = user_manager.verify_token(token)
        
        if payload:
            user_data = user_manager.get_user_by_id(payload['user_id'])
            if user_data:
                return jsonify({
                    'authenticated': True,
                    'user': user_data
                })
        
        return jsonify({'authenticated': False}), 401
            
    except Exception as e:
        # Removed logging for performance
        return jsonify({'authenticated': False}), 401

@app.route('/auth/refresh', methods=['POST'])
def refresh_token():
    """Refresh the access token using refresh token"""
    try:
        data = request.json
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return jsonify({'error': 'Refresh token is required'}), 400
        
        # Use our custom UserManager to verify and refresh the token
        from user_manager import user_manager
        payload = user_manager.verify_token(refresh_token)
        
        if payload and 'user_id' in payload:
            # Get user data
            user_data = user_manager.get_user_by_id(payload['user_id'])
            if user_data:
                # Generate new token
                new_token = user_manager.generate_token(
                    user_data['id'], 
                    user_data['email'], 
                    user_data['role']
                )
                
                # Calculate expiration time (7 days from now)
                from datetime import datetime, timedelta
                expires_at = (datetime.utcnow() + timedelta(days=7)).isoformat()
                
                return jsonify({
                    'success': True,
                    'access_token': new_token,
                    'refresh_token': new_token,  # For simplicity, use same token as refresh
                    'expires_at': expires_at
                })
        
        return jsonify({'error': 'Invalid refresh token'}), 401
        
    except Exception as e:
        # Removed logging for performance
        return jsonify({'error': 'Failed to refresh token'}), 401

# Serve static assets from dist folder in production
@app.route('/<path:filename>')
def serve_static(filename):
    if IS_DEVELOPMENT:
        return send_from_directory('static', filename)
    else:
        return send_from_directory('dist', filename)

@app.route('/api/transcribe_audio', methods=['POST'])
def transcribe_audio():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['file']
        if audio_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Use OpenAI Whisper API to transcribe
        audio_file.seek(0)  # Reset file pointer
        transcript = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="en"
        )
        
        return jsonify({
            'success': True,
            'text': transcript.text,
            'transcript': transcript.text
        })
        
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
