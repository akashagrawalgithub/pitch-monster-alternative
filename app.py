from flask import Flask, request, send_from_directory, jsonify, Response, stream_with_context
from flask_cors import CORS
from openai import OpenAI
import os
from datetime import datetime
import time
from prompts import agentPrompt, analysisPrompt, bestPitchPrompt
import asyncio
from cartesia import Cartesia
import base64
import numpy as np
import json
from backend_api import db_api
from supabase import create_client, Client

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://localhost:8000', 'https://pitch-monster-alternative.onrender.com'])

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
CARTESIA_API_KEY = os.environ.get("CARTESIA_API_KEY")


SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Cartesia client
cartesia_client = Cartesia(api_key=CARTESIA_API_KEY)

# Global conversation tracking
conversation_history = []
current_session_id = None
current_user_id = None

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
        print(f"Error processing raw audio: {e}")
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
        print(f"Error getting user ID: {e}")
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

@app.route('/conversation.html')
def conversation_page():
    if IS_DEVELOPMENT:
        # In development, serve from static folder
        return send_from_directory('static', 'conversation.html')
    else:
        # In production, serve from dist folder
        return send_from_directory('dist', 'conversation.html')

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
        print(f"TTS Error: {str(e)}")
        import traceback
        traceback.print_exc()
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
    global conversation_history
    
    user_input = request.json.get('message', '').strip()
    
    if not user_input:
        return jsonify({"reply": "I didn't catch that. Could you repeat?"})

    # Use up to the last 30 turns for context
    max_history = 30
    recent_history = conversation_history[-max_history:] if len(conversation_history) > max_history else conversation_history

    messages = [{
        "role": "system",
        "content": agentPrompt
    }]

    # Add recent conversation history
    for msg in recent_history:
        messages.append({"role": "user", "content": msg["user"]})
        messages.append({"role": "assistant", "content": msg["assistant"]})

    messages.append({"role": "user", "content": user_input})

    try:
        start_time = time.time()
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            max_tokens=70,
            temperature=0.3,  # Balanced for natural responses
            presence_penalty=0.6,
            frequency_penalty=0.4
        )
        
        reply = response.choices[0].message.content.strip()
        
        # Add to conversation history
        conversation_history.append({
            "user": user_input,
            "assistant": reply,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep history manageable (max 40 messages)
        if len(conversation_history) > 40:
            conversation_history = conversation_history[-40:]
        
        processing_time = time.time() - start_time
        print(f"Response time: {processing_time:.2f}s")
        
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
            print(f"Error: {str(e)}")
            return jsonify({"reply": "Sorry, I'm having trouble. Please try again."}), 500

@app.route('/chat_stream', methods=['POST'])
def chat_stream():
    global conversation_history
    
    user_input = request.json.get('message', '').strip()
    
    if not user_input:
        return Response('data: {"reply": "I didn\'t catch that. Could you repeat?"}\n\n', mimetype='text/event-stream')

    max_history = 30
    recent_history = conversation_history[-max_history:] if len(conversation_history) > max_history else conversation_history

    messages = [{
        "role": "system",
        "content": agentPrompt
    }]
    for msg in recent_history:
        messages.append({"role": "user", "content": msg["user"]})
        messages.append({"role": "assistant", "content": msg["assistant"]})
    messages.append({"role": "user", "content": user_input})

    def generate():
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=messages,
                max_tokens=50,
                temperature=0.3,
                presence_penalty=0.6,
                frequency_penalty=0.4,
                stream=True
            )
            full_reply = ""
            for chunk in response:
                delta = chunk.choices[0].delta.content
                if delta:
                    full_reply += delta
                    # Send as SSE event
                    yield f"data: {{\"reply\": \"{delta.replace('\\', '\\\\').replace('"', '\\\"')}\"}}\n\n"
            # Add to conversation history after streaming is done
            conversation_history.append({
                "user": user_input,
                "assistant": full_reply,
                "timestamp": datetime.now().isoformat()
            })
            if len(conversation_history) > 40:
                conversation_history[:] = conversation_history[-40:]
                
        except Exception as e:
            error_message = str(e).lower()
            if "rate limit" in error_message:
                yield 'data: {"reply": "Too many requests. Please wait a moment."}\n\n'
            elif "timeout" in error_message:
                yield 'data: {"reply": "Request timed out. Please try again."}\n\n'
            elif "api" in error_message:
                yield 'data: {"reply": "Service temporarily unavailable."}\n\n'
            else:
                print(f"Error: {str(e)}")
                yield 'data: {"reply": "Sorry, I\'m having trouble. Please try again."}\n\n'

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/analyze_conversation', methods=['POST'])
def analyze_conversation():
    """Analyze conversation transcript and return comprehensive feedback"""
    try:
        data = request.json
        transcript = data.get('transcript', [])
        
        if not transcript:
            return jsonify({"error": "No transcript provided"}), 400
        
        # Convert transcript to a readable format for analysis
        conversation_text = ""
        for i, exchange in enumerate(transcript, 1):
            sender = exchange.get('sender', 'Unknown')
            text = exchange.get('text', '')
            time_stamp = exchange.get('time', '')
            conversation_text += f"Exchange {i} ({time_stamp}):\n{sender}: {text}\n\n"
        
        # Prepare the analysis prompt with the conversation
        analysis_messages = [
            {
                "role": "system",
                "content": analysisPrompt
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
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {analysis_result}")
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
            print(f"Analysis error: {str(e)}")
            import traceback
            traceback.print_exc()
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
        
        # Call OpenAI for perfect pitch generation
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=3000,
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        perfect_pitch_result = response.choices[0].message.content.strip()
        try:
            perfect_pitch_data = json.loads(perfect_pitch_result)
            required_fields = ['perfect_conversation', 'overall_improvements', 'score_improvement']
            for field in required_fields:
                if field not in perfect_pitch_data:
                    return jsonify({"error": f"Missing required field: {field}"}), 500
            
            return jsonify(perfect_pitch_data)
            
        except json.JSONDecodeError as e:
            return jsonify({"error": "Invalid JSON response from perfect pitch generation"}), 500
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        
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
    """Supabase email/password login"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Authenticate with Supabase
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.user:
            return jsonify({
                'message': 'Login successful',
                'success': True,
                'user': {
                    'id': response.user.id,
                    'email': response.user.email,
                    'name': response.user.user_metadata.get('name', email.split('@')[0])
                },
                'access_token': response.session.access_token,
                'refresh_token': response.session.refresh_token,
                'expires_at': response.session.expires_at
            })
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/auth/check', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    try:
        auth_header = request.headers.get('Authorization')
        # print(f"Auth check - auth_header: {auth_header[:50] if auth_header else 'None'}...")
        
        if not auth_header or not auth_header.startswith('Bearer '):
            # print("Auth check - No valid auth header")
            return jsonify({'authenticated': False}), 401
        
        token = auth_header.split(' ')[1]
        # print(f"Auth check - token: {token[:50]}...")
        
        # Verify token with Supabase
        response = supabase.auth.get_user(token)
        # print(f"Auth check - response: {response}")
        # print(f"Auth check - response.user: {response.user if response else 'None'}")
        
        if response.user:
            user_data = {
                'id': response.user.id,
                'email': response.user.email,
                'name': response.user.user_metadata.get('name', response.user.email.split('@')[0])
            }
            # print(f"Auth check - user_data: {user_data}")
            return jsonify({
                'authenticated': True,
                'user': user_data
            })
        else:
            # print("Auth check - No user in response")
            return jsonify({'authenticated': False}), 401
            
    except Exception as e:
        print(f"Auth check error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'authenticated': False}), 401

@app.route('/auth/refresh', methods=['POST'])
def refresh_token():
    """Refresh the access token using refresh token"""
    try:
        data = request.json
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return jsonify({'error': 'Refresh token is required'}), 400
        
        # Refresh the token with Supabase
        response = supabase.auth.refresh_session(refresh_token)
        
        if response.session:
            return jsonify({
                'success': True,
                'access_token': response.session.access_token,
                'refresh_token': response.session.refresh_token,
                'expires_at': response.session.expires_at
            })
        else:
            return jsonify({'error': 'Failed to refresh token'}), 401
        
    except Exception as e:
        print(f"Token refresh error: {str(e)}")
        return jsonify({'error': 'Failed to refresh token'}), 401

# Serve static assets from dist folder in production
@app.route('/<path:filename>')
def serve_static(filename):
    if IS_DEVELOPMENT:
        return send_from_directory('static', filename)
    else:
        return send_from_directory('dist', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
