#!/bin/bash
# Quick start script for the backend
# Run from: research-assistant/backend/

set -e

echo "🔬 Multi-Agent Research Assistant — Backend Setup"
echo "================================================="

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+"
    exit 1
fi

# Create venv if not exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Install
echo "📥 Installing dependencies..."
pip install -r requirements.txt -q

# Check .env
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo "⚠️  Created .env from template."
    echo "   → Please edit backend/.env and add your GOOGLE_API_KEY"
    echo "   → Get a free key at: https://aistudio.google.com"
    echo ""
    read -p "Press Enter once you've added your API key..."
fi

echo ""
echo "✅ Starting FastAPI server at http://localhost:8000"
echo "   API docs: http://localhost:8000/docs"
echo ""
uvicorn main:app --reload --port 8000
