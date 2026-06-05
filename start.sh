#!/bin/bash

# Start Script for Android Local AI Agent

# Start Termux API (ensure it's active)
termux-wake-lock

# Start Ollama in the background if it's not running
if ! pgrep -x "ollama" > /dev/null
then
    echo "Starting Ollama..."
    ollama serve > logs/ollama.log 2>&1 &
    sleep 5
fi

# Activate virtual environment
source venv/bin/activate

# Start the bot
echo "Starting the agent..."
python main.py
