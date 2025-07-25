# Voice Web Chat Application

A modern, responsive voice chat application with beautiful animations and natural AI responses.

## Features

- 🎤 **Voice Recognition**: Real-time speech-to-text using Web Speech API
- 🔊 **Text-to-Speech**: Natural voice responses
- 🌊 **Voice Wave Animation**: Beautiful animated voice waves during listening
- ⚡ **Fast Responses**: Optimized for quick AI responses while maintaining natural conversation
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🎨 **Modern UI**: Glassmorphism design with gradient backgrounds
- ⌨️ **Keyboard Shortcuts**: Space to toggle, Escape to stop

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Open in Browser**:
   Navigate to `http://localhost:8000`

## Usage

- **Click the center button** to start voice chat
- **Speak clearly** into your microphone
- **Wait for AI response** (usually under 3 seconds)
- **Use "stop", "end", "quit", "exit", "goodbye", or "bye"** to end the session

## Keyboard Shortcuts

- **Space**: Toggle voice listening
- **Escape**: Stop listening

## Technical Details

- **Backend**: Flask with OpenAI GPT-3.5-turbo
- **Frontend**: Vanilla JavaScript with Web Speech API
- **Styling**: CSS3 with animations and glassmorphism effects
- **Optimization**: Balanced settings for natural responses with good performance

## Browser Compatibility

- Chrome (recommended)
- Edge
- Safari (limited support)
- Firefox (limited support)

## Notes

- Requires microphone access
- Works best with clear speech
- AI provides natural, conversational responses
- Conversation history is limited to 20 messages for performance 