#!/bin/bash

echo "🎤 Voice Web Chat Setup"
echo "======================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

echo "✅ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    echo "Please install pip3 and try again."
    exit 1
fi

echo "✅ pip3 found"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Check for Cartesia API key
if [ -z "$CARTESIA_API_KEY" ]; then
    echo ""
    echo "⚠️  Cartesia API key not found in environment variables"
    echo "Please set your Cartesia API key:"
    echo "export CARTESIA_API_KEY=\"your-api-key-here\""
    echo ""
    echo "Or add it directly to app.py (not recommended for production)"
    echo ""
    read -p "Do you want to continue without setting the API key? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled. Please set your API key and run setup again."
        exit 1
    fi
else
    echo "✅ Cartesia API key found in environment"
fi

# Check if Node.js is installed (optional)
if command -v node &> /dev/null; then
    echo "✅ Node.js found"
    if [ -f "package.json" ]; then
        echo "📦 Installing Node.js dependencies..."
        npm install
        if [ $? -eq 0 ]; then
            echo "✅ Node.js dependencies installed successfully"
        else
            echo "⚠️  Failed to install Node.js dependencies (optional)"
        fi
    fi
else
    echo "ℹ️  Node.js not found (optional for TypeScript compilation)"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo "python3 app.py"
echo ""
echo "Then open http://localhost:8000 in your browser"
echo ""
echo "For help, see README.md" 