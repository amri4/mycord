import os
from dotenv import find_dotenv, load_dotenv
from .bot import Bot
from .database import DB
from .tools import Tools
import discord
from discord.ext import commands as discord_commands

# Automatically load environment variables from .env when mycord is imported.
load_dotenv(find_dotenv())

# Expose discord.py helpers so users can mix mycord and discord.py imports.
commands = discord_commands

__all__ = ['Bot', 'DB', 'Tools', 'os', 'discord', 'commands']

import os
import sys
import requests
import subprocess

# ==============================================================================
# 🚀 AUTOMATIC WORKSPACE GENERATOR & SINGLE-BOOT SYNC
# ==============================================================================
cwd = os.getcwd()
txt_path = os.path.join(cwd, "setup.txt")
py_path = os.path.join(cwd, "setup.py")

created_any = False

# 📝 1. Generate setup.txt if missing
if not os.path.exists(txt_path):
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(
            "github_username=YOUR_USERNAME\n"
            "github_repo=YOUR_REPO_NAME\n"
            "ignore_files=setup.txt,.env,setup.py,data\n"
        )
    print("✨ [Mycord] Generated setup.txt in your file manager.")
    created_any = True

# ⚙️ 2. Generate setup.py if missing
if not os.path.exists(py_path):
    setup_script_content = """import os
import sys
import requests

if not os.path.exists("setup.txt"):
    print("❌ Missing setup.txt!")
    sys.exit(1)

config = {}
with open("setup.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and "=" in line:
            k, v = line.split("=", 1)
            config[k.strip()] = v.strip()

username = config.get("github_username")
repo = config.get("github_repo")
ignore_files = [x.strip() for x in config.get("ignore_files", "").split(",") if x.strip()]

if not username or username == "YOUR_USERNAME" or not repo or repo == "YOUR_REPO_NAME":
    print("❌ Please configure your GitHub details inside setup.txt first!")
    sys.exit(1)

print(f"🔄 Pulling latest files from {username}/{repo}...")
api_url = f"https://api.github.com/repos/{username}/{repo}/git/trees/HEAD?recursive=1"

try:
    res = requests.get(api_url)
    if res.status_code == 200:
        data = res.json()
        github_files = set()
        
        # Download Phase
        for item in data.get("tree", []):
            if item.get("type") == "blob":
                path = item["path"]
                github_files.add(path)
                if any(path == ignored or path.startswith(ignored.rstrip("/") + "/") for ignored in ignore_files):
                    continue
                folder = os.path.dirname(path)
                if folder:
                    os.makedirs(folder, exist_ok=True)
                raw_url = f"https://raw.githubusercontent.com/{username}/{repo}/HEAD/{path}"
                file_res = requests.get(raw_url)
                if file_res.status_code == 200:
                    with open(path, "wb") as f_out:
                        f_out.write(file_res.content)
                        
        # Cleanup Phase (Delete local files missing on GitHub)
        protected_files = {"setup.txt", ".env", "setup.py", "data"}
        for ignored in ignore_files:
            protected_files.add(ignored)
            
        for root, dirs, files in os.walk("."):
            if any(part.startswith('.') for part in root.split(os.sep)):
                continue
            for file in files:
                local_path = os.path.relpath(os.path.join(root, file), ".").replace("\\", "/")
                if local_path not in github_files and local_path not in protected_files:
                    try:
                        os.remove(local_path)
                        print(f"🗑️ [Mycord] Removed deleted file: {local_path}")
                    except Exception:
                        pass
        print("✅ Sync complete!")
except Exception as e:
    print(f"⚠️ Sync failed: {e}")
"""
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(setup_script_content)
    print("✨ [Mycord] Generated setup.py in your file manager.")
    created_any = True

# Stop execution on first boot so they can configure credentials
if created_any:
    print("👉 Please configure setup.txt with your GitHub details and restart the server.")
    sys.exit(0)

# ==============================================================================
# 🔄 THE ANTI-LOOP SYNC CHECK
# ==============================================================================
# We use an environment variable to mark that the update has already run.
# If it hasn't run yet, we run it and restart with the fresh code!
if os.environ.get("MYCORD_SYNCED") != "true":
    config = {}
    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line:
                k, v = line.split("=", 1)
                config[k.strip()] = v.strip()

    username = config.get("github_username")
    repo = config.get("github_repo")

    if username and username != "YOUR_USERNAME" and repo and repo != "YOUR_REPO_NAME":
        print(f"🔄 [Mycord] Pre-boot sync: Pulling updates from {username}/{repo}...")
        try:
            import setup
        except Exception as e:
            print(f"⚠️ [Mycord] Sync script error: {e}. Booting local files...")

    # Set the flag so the next process skips syncing and just runs the bot
    os.environ["MYCORD_SYNCED"] = "true"
    
    # Relaunch main.py now that the files are freshly updated
    print("🤖 [Mycord] Launching bot with updated files...")
    subprocess.run([sys.executable, "main.py"])
    sys.exit(0)  # Close this old process cleanly
