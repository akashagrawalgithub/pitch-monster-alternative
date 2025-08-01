from flask import Flask, request, send_from_directory, jsonify, Response, stream_with_context
import openai
import os
from datetime import datetime
import time
from prompts import agentPrompt
app = Flask(__name__)
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

conversation_history = []

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')
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
                model="gpt-4o-mini",
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
