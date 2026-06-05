import subprocess
import logging
from .shizuku import shizuku

logger = logging.getLogger(__name__)

def launch_app(package_name: str):
    """Launch an application by its package name"""
    logger.info(f"Launching app: {package_name}")
    # We can use monkey to launch the main activity
    cmd = f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
    if shizuku.is_available():
        return shizuku.execute(cmd)
    else:
        # Fallback to standard am if possible (often fails without root/shizuku in recent Android)
        try:
            res = subprocess.run(["am", "start", "-n", package_name], capture_output=True, text=True)
            return res.stdout
        except Exception as e:
            return str(e)

def force_stop_app(package_name: str):
    """Force stop an app (Requires Shizuku)"""
    logger.info(f"Force stopping app: {package_name}")
    if shizuku.is_available():
        return shizuku.execute(f"am force-stop {package_name}")
    return "Error: Shizuku required to force stop apps."

def search_installed_apps(keyword: str):
    """Search for installed packages matching the keyword"""
    cmd = "pm list packages"
    if shizuku.is_available():
        out = shizuku.execute(cmd)
    else:
        try:
            out = subprocess.run(cmd.split(), capture_output=True, text=True).stdout
        except:
            out = ""
            
    packages = []
    for line in out.splitlines():
        if line.startswith("package:"):
            pkg = line.replace("package:", "").strip()
            if keyword.lower() in pkg.lower():
                packages.append(pkg)
    return packages

def open_url(url: str):
    """Open a URL in the default browser"""
    cmd = f"am start -a android.intent.action.VIEW -d '{url}'"
    if shizuku.is_available():
        return shizuku.execute(cmd)
    else:
        try:
            res = subprocess.run(["am", "start", "-a", "android.intent.action.VIEW", "-d", url], capture_output=True, text=True)
            return res.stdout
        except Exception as e:
            return str(e)
