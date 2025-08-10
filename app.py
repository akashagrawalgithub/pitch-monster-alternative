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

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://localhost:8000'])

OPENAI_API_KEY = "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"
CARTESIA_API_KEY = "sk_car_VDpnj5rbG3FKJsfs4xrZyT"

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Cartesia client
cartesia_client = Cartesia(api_key=CARTESIA_API_KEY)

conversation_history = []

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
        
        perfect_pitch_prompt = bestPitchPrompt
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
                "content": perfect_pitch_prompt
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

# Serve static assets from dist folder in production
@app.route('/<path:filename>')
def serve_static(filename):
    if IS_DEVELOPMENT:
        return send_from_directory('static', filename)
    else:
        return send_from_directory('dist', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
