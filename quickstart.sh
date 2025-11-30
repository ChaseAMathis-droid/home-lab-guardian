#!/bin/bash

echo "🛡️  Home Lab Guardian - Quick Start"
echo "===================================="
echo ""

# Check if Python 3.11+ is available
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "❌ Python 3.9+ not found. Please install Python first."
    exit 1
fi

echo "✅ Using Python: $($PYTHON_CMD --version)"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv .venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -e ".[dev]"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env from template..."
    cp .env.example .env
    echo "💡 Edit .env to configure webhook URLs"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Install Ollama: https://ollama.ai/download"
echo "   2. Pull model: ollama pull llama3.1:8b"
echo "   3. Edit .env with your webhook URLs"
echo "   4. Run: hlg run --log-path sample_auth.log"
echo ""
echo "🧪 Test commands:"
echo "   hlg config          # Show configuration"
echo "   hlg test            # Test AI analyzer (requires Ollama)"
echo "   make test           # Run unit tests"
echo ""
