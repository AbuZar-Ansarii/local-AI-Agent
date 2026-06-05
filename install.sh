#!/bin/bash

# Android Local AI Agent - Termux Installation Script
# This script sets up the complete environment in Termux.

set -e

echo "Starting installation for Android Local AI Agent..."

# Update and upgrade packages
echo "Updating packages..."
pkg update -y && pkg upgrade -y

# Install essential dependencies
echo "Installing Python, Git, and build essentials..."
pkg install -y python git clang make libffi openssl binutils wget jq libjpeg-turbo nano

# Install Termux-API
echo "Installing Termux-API..."
pkg install -y termux-api

# Install Python packages
echo "Setting up Python virtual environment..."
python -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel setuptools

echo "Installing project dependencies from requirements.txt..."
pip install -r requirements.txt

# Install Ollama (Native Termux build if available, or fetch binary)
echo "Installing Ollama..."
# Ollama in Termux usually requires some specific setup. 
# We'll use the install script or standard binaries compatible with arm64.
curl -fsSL https://ollama.com/install.sh | sh || echo "Warning: Standard Ollama install failed. You may need to compile from source in Termux or use proot."

# Download Piper TTS binaries
echo "Setting up Piper TTS..."
mkdir -p tools/piper
cd tools/piper
wget -qO piper.tar.gz https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz || true
tar -xf piper.tar.gz || echo "Warning: Could not download Piper binaries automatically."
cd ../..

# Interactive Configuration
echo ""
echo "------------------------------------------------"
echo "  Configuration: Telegram Bot Setup"
echo "------------------------------------------------"
read -p "Enter your Telegram Bot Token: " bot_token
read -p "Enter your Telegram User ID (for whitelist): " user_id

cat <<EOF > .env
TELEGRAM_BOT_TOKEN=$bot_token
ALLOWED_USER_IDS=$user_id
OLLAMA_HOST=http://localhost:11434
MODEL_NAME=llama3
EMBEDDING_MODEL=nomic-embed-text
WHISPER_MODEL=base
PIPER_MODEL=en_US-lessac-medium
SHIZUKU_ENABLED=true
LOG_LEVEL=INFO
EOF

echo "Configuration saved to .env file."
echo "Setup complete! You can now run the agent with: ./start.sh"
