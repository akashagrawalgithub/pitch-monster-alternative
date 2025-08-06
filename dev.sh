#!/bin/bash

# Development script to run both frontend and backend

echo "🚀 Starting Voice Web Chat Development Environment..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Set Flask environment to development
export FLASK_ENV=development

# Start Flask backend in background
echo "🐍 Starting Flask backend on port 8000..."
python3 app.py &
FLASK_PID=$!

# Wait a moment for Flask to start
sleep 2

# Start Vite dev server
echo "⚡ Starting Vite dev server on port 3000..."
npm run dev &
VITE_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "🛑 Shutting down development servers..."
    kill $FLASK_PID 2>/dev/null
    kill $VITE_PID 2>/dev/null
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup SIGINT

echo "✅ Development environment is running!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "📊 Analysis: http://localhost:3000/analysis.html"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for both processes
wait 