# Voice Web Chat - Import/Export Analytics Consultant

A real-time voice chat application with AI-powered responses and high-quality text-to-speech using Cartesia.

## Features

- 🎤 Real-time speech recognition
- 🤖 AI-powered responses with streaming
- 🔊 High-quality TTS using Cartesia
- 📱 Responsive design with voice wave animations
- 💬 Conversation transcript with timestamps
- 🌊 Immersive UI with ocean animations

## Setup

### Prerequisites

- Python 3.8+
- Node.js (for TypeScript compilation)
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

3. **Set up Cartesia API key**
   
   Get your API key from [Cartesia](https://cartesia.ai) and set it as an environment variable:
   
   ```bash
   export CARTESIA_API_KEY="your-cartesia-api-key-here"
   ```
   
   Or add it directly to `app.py` (not recommended for production):
   ```python
   CARTESIA_API_KEY = "your-actual-cartesia-api-key"
   ```

4. **Install TypeScript dependencies (optional)**
   ```bash
   npm install
   ```

### Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:8000`

3. **Start chatting**
   Click the microphone button to begin voice conversation

## API Endpoints

- `GET /` - Main application page
- `POST /chat` - Non-streaming chat endpoint
- `POST /chat_stream` - Streaming chat endpoint (SSE)
- `POST /tts` - Text-to-speech generation
- `POST /tts_stream` - Streaming TTS (SSE)
- `GET /voices` - List available Cartesia voices
- `GET /health` - Health check

## Configuration

### Cartesia Voice Settings

The application uses Cartesia's `sonic-2` model with default voice settings. You can customize:

- **Voice ID**: Change the default voice ID in `app.py`
- **Model**: Switch between different Cartesia models
- **Audio Format**: Modify sample rate and encoding

### OpenAI Settings

- **Model**: Currently using `gpt-4o-mini`
- **Max Tokens**: 70 (optimized for concise responses)
- **Temperature**: 0.3 (balanced creativity)

## Architecture

### Backend (Flask)
- **Speech Processing**: OpenAI Whisper API
- **Text-to-Speech**: Cartesia Python SDK
- **AI Responses**: OpenAI GPT-4
- **Streaming**: Server-Sent Events (SSE)

### Frontend (TypeScript)
- **Speech Recognition**: Web Speech API
- **Audio Playback**: Web Audio API
- **UI**: Dynamic DOM manipulation with CSS animations
- **Real-time Updates**: EventSource for streaming

## Troubleshooting

### Common Issues

1. **Cartesia API Key Error**
   - Ensure your API key is valid and has sufficient credits
   - Check the key is properly set in environment variables

2. **Audio Playback Issues**
   - Ensure browser supports Web Audio API
   - Check browser permissions for microphone access

3. **Speech Recognition Not Working**
   - Use HTTPS in production (required for Web Speech API)
   - Ensure microphone permissions are granted

### Performance Tips

- Use a good internet connection for optimal streaming
- Close other audio applications to prevent conflicts
- Consider using a dedicated voice for better TTS quality

## Development

### Adding New Voices

1. Get available voices:
   ```bash
   curl http://localhost:8000/voices
   ```

2. Update the voice ID in `app.py`:
   ```python
   voice={
       "mode": "id",
       "id": "your-preferred-voice-id",
   }
   ```

### Customizing the AI Personality

Edit `prompts.py` to modify the AI's role and behavior.

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request 