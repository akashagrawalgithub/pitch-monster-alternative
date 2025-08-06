# Voice Web Chat - Dynamic Sales Training Analysis

A comprehensive voice-based sales training platform with dynamic AI-powered conversation analysis.

## Features

### 🎯 Dynamic Conversation Analysis
- **Real-time Analysis**: Analyzes conversations as they happen
- **Comprehensive Feedback**: Provides detailed insights on sales skills, voice delivery, and process flow
- **Edge Case Handling**: Gracefully handles short conversations, incomplete calls, and various scenarios
- **JSON-based Responses**: Structured data format for easy customization and UI updates

### 🎤 Voice Interaction
- **Real-time Speech Recognition**: Uses Web Speech API for instant voice input
- **AI Voice Response**: Cartesia TTS for natural-sounding AI responses
- **Voice Recording**: Captures entire conversations for playback and analysis
- **Audio Mixing**: Combines user and AI audio for complete conversation recording

### 📊 Analysis Components

#### Sales Skills Assessment (1-5 Stars)
- **Introduction Quality**: Opening and rapport building
- **Need Analysis**: Discovery questions and understanding
- **Objection Handling**: Addressing concerns effectively
- **Closing Skills**: Creating urgency and asking for commitment

#### Voice & Delivery Analysis (0-100%)
- **Grammar & Clarity**: Proper sentence structure and pronunciation
- **Fluency & Flow**: Smooth speech without interruptions
- **Confidence Level**: Reduced hesitation and uncertainty
- **Speaking Pace**: Optimal speed for understanding
- **Enthusiasm**: Energy and passion in delivery
- **Message Clarity**: Clear and understandable communication

#### Sales Process Flow
- **Introduction**: Initial contact and rapport building
- **Discovery**: Understanding customer needs and pain points
- **Presentation**: Presenting solutions and value propositions
- **Objection Handling**: Addressing concerns and objections
- **Close**: Securing commitment and next steps

## Technical Architecture

### Backend (Flask)
- **Dynamic Analysis Endpoint**: `/analyze_conversation` - Processes conversation transcripts
- **TTS Integration**: Cartesia API for high-quality voice synthesis
- **JSON Response Format**: Structured analysis data for frontend consumption

### Frontend (TypeScript/HTML)
- **Real-time UI Updates**: Dynamic loading and display of analysis results
- **Session Storage**: Maintains conversation data across pages
- **Responsive Design**: Works on desktop and mobile devices

### Analysis Prompt System
- **Comprehensive Guidelines**: Detailed instructions for AI analysis
- **Edge Case Handling**: Specific instructions for various conversation scenarios
- **Consistent JSON Format**: Ensures reliable data structure

## Setup and Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key
- Cartesia API key

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd voice-web-chat
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Node.js dependencies**
```bash
npm install
```

4. **Set up environment variables**
```bash
export OPENAI_API_KEY="your-openai-api-key"
export CARTESIA_API_KEY="your-cartesia-api-key"
```

5. **Run the development server**
```bash
# Terminal 1: Flask backend
python app.py

# Terminal 2: Vite frontend (optional for development)
npm run dev
```

## Usage

### Basic Workflow

1. **Start a Conversation**
   - Click the microphone button to begin
   - Speak naturally with the AI sales trainer
   - The system records both your voice and AI responses

2. **Complete the Session**
   - Click the microphone button again to end
   - You'll be redirected to the success page
   - After 3 seconds, you'll see the analysis page

3. **Review Analysis**
   - View comprehensive feedback on your performance
   - See scores for different sales skills
   - Review strengths and areas for improvement

### Testing the Analysis System

Visit `/test_analysis.html` to test the analysis system:

- **Sample Data Test**: Tests with predefined conversation data
- **Session Data Test**: Tests with your actual conversation transcript
- **Status Check**: Verifies the analysis endpoint is working

## API Endpoints

### Analysis Endpoints

#### POST `/analyze_conversation`
Analyzes a conversation transcript and returns comprehensive feedback.

**Request Body:**
```json
{
  "transcript": [
    {
      "sender": "AI",
      "text": "Hello, how can I help you today?",
      "time": "00:00"
    },
    {
      "sender": "You", 
      "text": "I'm interested in your product",
      "time": "00:05"
    }
  ]
}
```

**Response:**
```json
{
  "session_info": {
    "scenario_type": "Discovery Call",
    "prospect_role": "Decision Maker",
    "conversation_stage": "Introduction",
    "duration_minutes": 5,
    "total_exchanges": 10,
    "confidence_level": 85
  },
  "overall_score": {
    "percentage": 87,
    "grade": "B+"
  },
  "key_metrics": {
    "conversation_time": "5m 30s",
    "exchanges": 10,
    "avg_response_time": "2.3s"
  },
  "voice_delivery_analysis": {
    "grammar_clarity": {
      "score": 92,
      "description": "Excellent grammar and clear pronunciation"
    }
  },
  "sales_skills_assessment": {
    "introduction_quality": {
      "stars": 4,
      "score": 4.2,
      "description": "Strong opening with good rapport building"
    }
  },
  "sales_process_flow": {
    "introduction": {
      "status": "completed",
      "score": 92,
      "description": "Effective introduction and rapport building"
    }
  },
  "strengths": [
    "Excellent objection handling with specific examples",
    "Strong use of quantified value propositions"
  ],
  "improvements": [
    "Spend more time on discovery before presenting solutions",
    "Work on closing techniques and creating urgency"
  ]
}
```

#### GET `/test_analysis`
Test endpoint that uses sample data to verify the analysis system.

### TTS Endpoints

#### POST `/tts`
Generates speech from text using Cartesia.

#### POST `/tts_stream`
Streams TTS audio for real-time playback.

## Edge Cases Handled

### Short Conversations (1-2 exchanges)
- Minimal scores for skills not demonstrated
- Focus on basic communication quality
- Appropriate feedback for brief interactions

### Incomplete Conversations
- Marks incomplete sales stages appropriately
- Provides feedback on what was accomplished
- Suggests areas for future improvement

### One-sided Conversations
- Scores based on available responses
- Identifies missing elements
- Provides guidance for balanced interactions

### Technical Issues
- Graceful handling of audio recording failures
- Fallback to text-only analysis when needed
- Error recovery and user feedback

## Customization

### Modifying Analysis Criteria

The analysis system uses a comprehensive prompt in `prompts.py`. To customize:

1. **Edit the `analysisPrompt`** in `prompts.py`
2. **Modify the JSON structure** to add new metrics
3. **Update the frontend** to display new analysis components

### Adding New Analysis Metrics

1. **Update the JSON schema** in the analysis prompt
2. **Add corresponding UI elements** in `analysis.html`
3. **Implement update functions** for the new metrics

### Changing Scoring Algorithms

The analysis prompt includes detailed scoring guidelines. Modify the prompt to:

- Adjust scoring criteria for different skills
- Change the weighting of various factors
- Add new evaluation dimensions

## Troubleshooting

### Common Issues

1. **Analysis not loading**
   - Check browser console for errors
   - Verify the `/analyze_conversation` endpoint is accessible
   - Ensure transcript data is available in sessionStorage

2. **Audio recording issues**
   - Check microphone permissions
   - Verify browser supports MediaRecorder API
   - Test with different browsers

3. **TTS not working**
   - Verify Cartesia API key is valid
   - Check network connectivity
   - Review browser console for errors

### Debug Mode

Enable debug logging by setting:
```bash
export FLASK_ENV=development
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with the test page
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 