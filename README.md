# Android Local AI Agent

A completely local AI agent running on Android via Termux, controllable through Telegram.

## Features

- **Local Execution:** Uses Ollama to run models (gemma3, qwen3, llama3) locally on your Android device.
- **Remote Control:** Securely control your device via Telegram.
- **Android Tools:** Control WiFi, Bluetooth, Screen Brightness, Notifications, Media, and Apps.
- **Shizuku Integration:** Perform privileged tasks using Shizuku.
- **Voice Interaction:** STT via Faster-Whisper and TTS via Piper.
- **Long-Term Memory:** ChromaDB stores user preferences and contexts.

## Setup Instructions

1. Install Termux and Termux:API from F-Droid.
2. Install Shizuku and start it (via adb or wireless debugging).
3. Clone this repository in Termux.
4. Run `./install.sh`.
5. Create a Telegram bot using BotFather and get your bot token.
6. Get your Telegram User ID (e.g., from userinfobot).
7. Create a `.env` file:
   ```env
   TELEGRAM_BOT_TOKEN=your_token
   ALLOWED_USER_IDS=123456789
   ```
8. Run `./start.sh`.
