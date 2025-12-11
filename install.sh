#!/bin/bash

# Installation script for C++ Analysis Agent
# For Ubuntu Server 24.04

set -e

echo "=================================="
echo "C++ Analysis Agent - Installation"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "Error: Python 3.11+ is required"
    exit 1
fi

# Check pip
echo "Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 not found"
    exit 1
fi

pip_version=$(pip3 --version | awk '{print $2}')
echo "pip version: $pip_version"

# Check Ollama
echo ""
echo "Checking Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "Warning: Ollama not found in PATH"
    echo "Please ensure Ollama is installed and running"
else
    ollama --version
fi

# Check if Ollama is running
echo "Checking if Ollama server is running..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama server is running"
else
    echo "Warning: Ollama server not responding on http://localhost:11434"
    echo "Please start Ollama: ollama serve"
fi

# Install Graphviz
echo ""
echo "Checking Graphviz..."
if ! command -v dot &> /dev/null; then
    echo "Graphviz not found. Installing..."
    sudo apt update
    sudo apt install -y graphviz
    echo "✓ Graphviz installed"
else
    echo "✓ Graphviz is already installed"
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "=================================="
echo "Installation Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Verify Ollama models are available:"
echo "   ollama list"
echo ""
echo "2. If needed, pull models:"
echo "   ollama pull qwen2.5"
echo "   ollama pull jina/jina-embeddings-v2-base-en"
echo ""
echo "3. Review configuration:"
echo "   nano config.yaml"
echo ""
echo "4. Run the agent:"
echo "   python3 main.py analyze /path/to/cpp/project"
echo ""
echo "For more information, see README.md"

