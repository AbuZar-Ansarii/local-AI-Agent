# Android Local AI Agent

A production-grade, fully local AI agent that runs on Android through **Termux** and is controlled remotely via **Telegram**. This agent utilizes local LLMs (Ollama), supports long-term memory (ChromaDB), and performs privileged Android operations using **Shizuku**.

---

## 📂 Project Structure

```text
android_local_agent/
├── agent/               # The "Brain" of the Agent
│   ├── graph.py         # LangGraph workflow and orchestration logic
│   ├── tools.py         # Definitions of tools (Apps, WiFi, Memory, etc.)
│   ├── memory.py        # Short-term conversation history management
│   ├── prompts.py       # System instructions for the LLM
│   └── state.py         # Type definitions for the agent's cognitive state
├── android/             # Android Control Layer
│   ├── termux_api.py    # Interface for battery, notifications, and hardware
│   ├── shizuku.py       # Privileged ADB command execution bridge
│   ├── intents.py       # App launching and activity management
│   └── accessibility.py # UI interaction and automation skeleton
├── telegram/            # Remote Interface Layer
│   ├── bot.py           # Telegram bot initialization and polling setup
│   └── handlers.py      # Logic for messages, commands, and media
├── memory/              # Long-Term Memory Layer
│   └── chroma_db.py     # Local vector database for user preferences
├── config/              # Configuration Management
│   └── settings.py      # Global settings and environment variable parsing
├── docs/                # Project documentation and architecture plans
├── tests/               # Unit tests for tools and logic
├── main.py              # Application entry point
├── install.sh           # Interactive setup script for Termux
├── start.sh             # Execution script to launch the bot and Ollama
├── requirements.txt     # Python dependencies
└── README.md            # User guide and documentation
```

---

## 🚀 Step-by-Step Guide

### 1. Prerequisites (On Android)
*   **Termux:** Install from [F-Droid](https://f-droid.org/en/packages/com.termux/).
*   **Termux:API:** Install from [F-Droid](https://f-droid.org/en/packages/com.termux.api/).
*   **Shizuku:** Install from Play Store or GitHub. Start it using Wireless Debugging or ADB.

### 2. Prepare the Environment
Open Termux and run the following commands:
```bash
# Allow storage access
termux-setup-storage

# Clone the repository
git clone https://github.com/AbuZar-Ansarii/local-AI-Agent.git
cd local-AI-Agent/android_local_agent
```

### 3. Interactive Installation
Run the installer. It will update system packages, install Python, Ollama, and set up your configuration.
```bash
chmod +x install.sh start.sh
./install.sh
```
**During installation, the script will ask for:**
1.  **Telegram Bot Token:** Create one via [@BotFather](https://t.me/botfather).
2.  **Telegram User ID:** Get yours from [@userinfobot](https://t.me/userinfobot). This ensures only *you* can control your phone.

### 4. Start the Agent
Ensure Shizuku is running, then start the agent:
```bash
./start.sh
```

### 5. Using the Agent via Telegram
Open your bot on Telegram and start chatting!

**Example Commands:**
*   *"Open YouTube and search for Lo-fi music"*
*   *"What is my battery percentage?"*
*   *"Turn off the WiFi"*
*   *"Set screen brightness to 50%"*
*   *"Take a screenshot"* (requires `/screenshot` command or natural language)
*   *"Remember that I like Dark Mode"* (Saves to long-term memory)

---

## 🛠 Features in Detail

*   **Autonomous Planning:** Uses LangGraph to plan multi-step tasks (e.g., search web -> open app -> perform action).
*   **Secure Access:** Whitelist-based security ensures only your Telegram ID has control.
*   **Privileged Control:** Uses Shizuku to execute ADB-level commands without requiring a rooted device.
*   **Local-First:** All processing (LLM, Embeddings, Database) happens on your device. No data leaves your phone except for Telegram communication.

---

## 🤝 Contributing
Contributions are welcome! Please follow the existing code style and provide tests for new features.

## 📜 License
MIT License.

# ********************************************************************************************************************

```
pkg update && pkg upgrade -y
pkg install proot-distro -y
```
```
proot-distro install debian
proot-distro login debian
```
```
apt update && apt upgrade -y
apt install git python3 python3-pip python3-venv libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 -y
```
```
git clone https://github.com/FoundationAgents/OpenManus.git
cd OpenManus
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
```
playwright install chromium
```
## Method B

```
pkg update && pkg upgrade -y
pkg install git python python-pip clang make libjpeg-turbo -y
```

```
git clone https://github.com/FoundationAgents/OpenManus.git
cd OpenManus
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```
cp config/config.example.toml config/config.toml
nano config/config.toml
```
### LLm config
```
[llm]
model = "gemini-2.5-flash"
api_key = "YOUR_GEMINI_API_KEY"
base_url = "https://generativelanguage.googleapis.com/v1beta"
```
```
python run.py
```
