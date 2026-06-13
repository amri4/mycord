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


import sys

def init_workspace():
    """
    Generates both setup.txt and setup.py automatically 
    in the directory where the bot is being run.
    """
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
        # This is the exact code that will be written inside their new setup.py file
        setup_script_content = """import os
import sys
import requests
import subprocess

# Load configuration from setup.txt
if not os.path.exists("setup.txt"):
    print("❌ Missing setup.txt! Please run your main script to generate it.")
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
        
        # Download files
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
                        
        print("✅ Sync complete!")
except Exception as e:
    print(f"⚠️ Sync failed: {e}")
"""
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(setup_script_content)
        print("✨ [Mycord] Generated setup.py in your file manager.")
        created_any = True

    # If we had to create either file, pause execution so the user can fill in setup.txt
    if created_any:
        print("👉 Please configure setup.txt with your GitHub details and restart.")
        sys.exit(0)
