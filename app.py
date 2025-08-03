from flask import Flask, request, send_from_directory, jsonify, Response, stream_with_context
import openai
import os
from datetime import datetime
import time
from prompts import agentPrompt
import asyncio
from cartesia import Cartesia
import base64
import numpy as np

app = Flask(__name__)
OPENAI_API_KEY = "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"
CARTESIA_API_KEY = "sk_car_VDpnj5rbG3FKJsfs4xrZyT"

openai.api_key = OPENAI_API_KEY

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

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/analysis.html')
def analysis():
    return send_from_directory('static', 'analysis.html')

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

@app.route('/voices', methods=['GET'])
def list_voices():
    """List available Cartesia voices"""
    try:
        voices = list(cartesia_client.voices.list())
        voice_list = []
        for voice in voices:
            voice_list.append({
                "id": voice.id,
                "name": voice.name,
                "language": voice.language,
                "description": voice.description
            })
        return jsonify({"voices": voice_list})
    except Exception as e:
        print(f"Error listing voices: {str(e)}")
        return jsonify({"error": "Failed to list voices"}), 500

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
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
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

    except openai.error.RateLimitError:
        return jsonify({"reply": "Too many requests. Please wait a moment."}), 429
    except openai.error.Timeout:
        return jsonify({"reply": "Request timed out. Please try again."}), 408
    except openai.error.APIError as e:
        return jsonify({"reply": "Service temporarily unavailable."}), 503
    except Exception as e:
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
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125",
                messages=messages,
                max_tokens=70,
                temperature=0.3,
                presence_penalty=0.6,
                frequency_penalty=0.4,
                stream=True
            )
            full_reply = ""
            for chunk in response:
                delta = chunk["choices"][0]["delta"].get("content", "")
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
        except openai.error.RateLimitError:
            yield 'data: {"reply": "Too many requests. Please wait a moment."}\n\n'
        except openai.error.Timeout:
            yield 'data: {"reply": "Request timed out. Please try again."}\n\n'
        except openai.error.APIError as e:
            yield 'data: {"reply": "Service temporarily unavailable."}\n\n'
        except Exception as e:
            print(f"Error: {str(e)}")
            yield 'data: {"reply": "Sorry, I\'m having trouble. Please try again."}\n\n'

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
