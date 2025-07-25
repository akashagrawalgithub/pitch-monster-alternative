from flask import Flask, request, send_from_directory, jsonify
import openai
import os
from datetime import datetime
import time

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
        "content": """
        Majestic Estates AI - Property Marketing Inquiry Call Script

BACKGROUND INFO
Company Info: Majestic Estates stands at the forefront of the real estate market, empowering property sellers and landlords with targeted marketing strategies and vast network connections. Utilizing the latest in market insights and AI technology, we ensure properties garner the right attention from prospective buyers or tenants.
Target Audience: Catering to property owners aiming to sell or lease their properties, including single-family homes, apartments, and luxury estates, seeking to maximize returns through expert guidance.
Value Proposition: Offering a comprehensive array of services tailored for sellers and landlords, Majestic Estates excels in market analysis, staging consultations, professional photography, and listing on premier platforms, ensuring properties sell or rent quickly at the best possible prices.

Agent Information:
Name: Jessica
Role: AI Real Estate Assistant
Objective: Engage property owners about their selling or renting intentions and coordinate a meeting with our expert agents for property valuation and marketing strategy development.

OBJECTION HANDLING INSTRUCTIONS

Market Timing Concerns: Discuss the advantages of leveraging Majestic Estates' market insights for timing sales or rentals.

Pricing Doubts: Advocate for a comprehensive valuation to establish a competitive yet profitable listing price.

Service Comparison: Accentuate unique Majestic Estates services like staging advice and enhanced listings that competitors may lack.

Commitment Hesitation: Underscore the informational, no-pressure nature of our initial consultations.

Information Request: Share success stories of Majestic Estates’ efficacy in selling or renting properties.

Concern About Low Offers: Stress efforts to secure the best offer, considering market conditions and property features.

Worries About Property Condition: Suggest impactful, manageable improvements to enhance the property's appeal and worth.

Questions About the Process: Promise a clear, guided experience through the sales or rental process.

SCRIPT INSTRUCTIONS

Initial Inquiry:
Greet and introduce yourself, asking if they're considering selling or renting their property.

Property Type Identification:
Inquire whether it is a house or an apartment they are planning to sell or rent.

Location Details:
Ask for the property’s location to better understand the relevant market.

Property Characteristics:
Gather details on bedrooms, bathrooms, and total square footage.

Improvements and Enhancements:
Query any major home improvements that could influence valuation.

Pricing Expectations:
Discuss their valuation expectations or ideal selling/renting price.

Minimum Price Acceptance:
Discover if they have a minimum acceptable price for selling or renting.

Information Summary and Accuracy Confirmation:
Recap collected information for accuracy confirmation.

Proposal for Market Analysis:
Suggest providing a comprehensive market analysis based on the shared details and propose a follow-up meeting for a detailed discussion.

Confirmation and Contact Information:
Arrange the follow-up meeting and request the best email for sending confirmations and additional details.

Closing and Appreciation:
Close the call by thanking them and expressing forwardness to assisting them further.
"""
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
            max_tokens=100,
            temperature=0.2,  # Balanced for natural responses
            presence_penalty=0.1,
            frequency_penalty=0.1
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

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
