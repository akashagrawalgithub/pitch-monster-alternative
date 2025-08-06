#!/bin/bash

# Production build script

echo "🏗️ Building Voice Web Chat for production..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Build the frontend
echo "⚡ Building frontend with Vite..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Frontend build completed successfully!"
    echo "📁 Build output: ./dist/"
    echo ""
    echo "🚀 To run in production:"
    echo "   python3 app.py"
    echo ""
    echo "📱 Access the app at: http://localhost:5000"
else
    echo "❌ Build failed!"
    exit 1
fi 