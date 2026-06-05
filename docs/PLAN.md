# Android Local AI Agent - Implementation Plan & Architecture

## Architecture

The system is designed as a modular, local-first agentic platform operating on Android via Termux. It has four main layers:

1. **Interface Layer (Telegram Bot):** Provides remote interaction, authentication, voice/text parsing, and multimedia handling.
2. **Cognitive Layer (LangGraph & Ollama):** The "brain" of the agent, responsible for intent parsing, planning, tool selection, memory retrieval, and final response generation.
3. **Memory Layer (ChromaDB):** Stores long-term user preferences, past interactions, and operational context in a local vector database.
4. **Execution Layer (Android Control):** Connects to the host OS using Termux APIs, Android Intents, Accessibility Services, and Shizuku (ADB) to perform privileged system operations.

## Directory Structure

```text
android_local_agent/
├── agent/
│   ├── graph.py        # LangGraph workflow definitions
│   ├── tools.py        # Integration of Android and Web tools for the LLM
│   ├── memory.py       # Short-term memory management for LangGraph state
│   ├── prompts.py      # System prompts and templates
│   └── state.py        # Type definitions for the agent's state
├── telegram/
│   ├── bot.py          # Main Telegram bot initialization
│   └── handlers.py     # Message, command, voice, and media handlers
├── android/
│   ├── intents.py      # Android intent constructor and executor
│   ├── shizuku.py      # ADB/Shizuku privileged command execution
│   ├── accessibility.py# Accessibility service interactions (if applicable)
│   └── termux_api.py   # Termux-api wrappers for battery, notifications, etc.
├── memory/
│   └── chroma_db.py    # Vector database operations for long-term memory
├── config/
│   └── settings.py     # Configuration, environment variables, whitelist
├── logs/               # Application logs directory
├── tests/              # Unit and integration tests
├── main.py             # Entry point integrating all modules
├── requirements.txt    # Python dependencies
├── install.sh          # Setup script for Termux
├── start.sh            # Run script
└── README.md           # Documentation
```

## Implementation Plan

We will incrementally construct the project file-by-file:

*   **Phase 1: Foundation & Tooling**
    *   Create configuration (`config/settings.py`)
    *   Setup Python dependencies (`requirements.txt`)
    *   Develop setup and run scripts (`install.sh`, `start.sh`)
    *   Write the primary `README.md`
*   **Phase 2: Android Execution Layer**
    *   Develop `android/termux_api.py`
    *   Develop `android/shizuku.py`
    *   Develop `android/intents.py`
    *   Develop `android/accessibility.py`
*   **Phase 3: Memory & State Management**
    *   Implement long-term memory `memory/chroma_db.py`
    *   Define agent state `agent/state.py`
    *   Define agent prompts `agent/prompts.py`
*   **Phase 4: Agent & Tool Calling**
    *   Bind Android & Web tools `agent/tools.py`
    *   Implement short-term memory `agent/memory.py`
    *   Build the LangGraph execution flow `agent/graph.py`
*   **Phase 5: Interface & Orchestration**
    *   Implement Telegram Handlers `telegram/handlers.py`
    *   Implement Telegram Bot `telegram/bot.py`
    *   Create the main entry point `main.py`
