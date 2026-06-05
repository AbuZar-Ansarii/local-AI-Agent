from langchain_core.tools import tool
import subprocess
from android import termux_api, intents, shizuku
from memory.chroma_db import memory_db

@tool
def open_app(package_name: str) -> str:
    """Open an Android application by its package name (e.g., com.android.chrome)."""
    return intents.launch_app(package_name)

@tool
def close_app(package_name: str) -> str:
    """Force stop an Android application by its package name."""
    return intents.force_stop_app(package_name)

@tool
def search_app(keyword: str) -> str:
    """Search for installed apps matching a keyword."""
    apps = intents.search_installed_apps(keyword)
    return f"Found packages: {', '.join(apps)}" if apps else "No matching packages found."

@tool
def toggle_wifi(enable: bool) -> str:
    """Enable or disable WiFi."""
    return termux_api.toggle_wifi(enable)

@tool
def toggle_bluetooth(enable: bool) -> str:
    """Enable or disable Bluetooth (Uses standard Android intent if Termux API unsupported, or Shizuku)."""
    # Simple implementation via shell
    state = "1" if enable else "0"
    if shizuku.shizuku.is_available():
        return shizuku.shizuku.execute(f"cmd bluetooth_manager {'enable' if enable else 'disable'}")
    return "Bluetooth toggling requires Shizuku."

@tool
def set_brightness(level: int) -> str:
    """Set screen brightness between 0 and 255."""
    return termux_api.set_brightness(level)

@tool
def get_battery() -> str:
    """Get the current battery level and status."""
    return str(termux_api.get_battery())

@tool
def get_notifications() -> str:
    """Read the active notifications on the device."""
    return str(termux_api.get_notifications())

@tool
def take_screenshot(filepath: str = "/sdcard/screenshot.png") -> str:
    """Take a screenshot and save it to the specified filepath."""
    return shizuku.shizuku.take_screenshot(filepath)

@tool
def execute_shell_command(command: str) -> str:
    """Execute a general shell command in Termux."""
    try:
        res = subprocess.run(command, shell=True, capture_output=True, text=True)
        return res.stdout if res.returncode == 0 else f"Error: {res.stderr}"
    except Exception as e:
        return str(e)

@tool
def read_file(filepath: str) -> str:
    """Read contents of a file."""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return str(e)

@tool
def write_file(filepath: str, content: str) -> str:
    """Write contents to a file."""
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return str(e)

@tool
def save_memory(memory_id: str, content: str) -> str:
    """Save information to long term memory for future reference."""
    return memory_db.save_memory(memory_id, content)

@tool
def search_memory(query: str) -> str:
    """Search long term memory for context or user preferences."""
    results = memory_db.search_memory(query)
    return str(results)

@tool
def delete_memory(memory_id: str) -> str:
    """Delete a specific memory by its ID."""
    return memory_db.delete_memory(memory_id)

@tool
def search_web(query: str) -> str:
    """Search the web for information using DuckDuckGo HTML."""
    try:
        import requests
        from bs4 import BeautifulSoup
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://html.duckduckgo.com/html/?q={query}"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        results = soup.find_all('a', class_='result__snippet')
        texts = [r.get_text() for r in results[:3]]
        return "\n".join(texts) if texts else "No results found."
    except Exception as e:
        return str(e)

# Collect all tools
agent_tools = [
    open_app, close_app, search_app, toggle_wifi, toggle_bluetooth,
    set_brightness, get_battery, get_notifications, take_screenshot,
    execute_shell_command, read_file, write_file, save_memory,
    search_memory, delete_memory, search_web
]
