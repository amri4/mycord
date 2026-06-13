import os
import sys
from setuptools import setup
from setuptools.command.install import install

# ==============================================================================
# 🚀 AUTOMATIC INSTALLATION HOOK
# ==============================================================================
class CustomInstallCommand(install):
    """This runs automatically the exact moment someone types 'pip install mycord'"""
    def run(self):
        # 1. Run the standard pip installation first
        install.run(self)
        
        # 2. Find where the user is executing the command (their File Manager root)
        cwd = os.getcwd()
        setup_file_path = os.path.join(cwd, "setup.txt")
        
        # 3. Automatically drop setup.txt right into their folder
        if not os.path.exists(setup_file_path):
            with open(setup_file_path, "w", encoding="utf-8") as f:
                f.write(
                    "github_username=YOUR_USERNAME\n"
                    "github_repo=YOUR_REPO_NAME\n"
                    "ignore_files=setup.txt,.env,data\n"
                )
            print("\n✨ [Mycord] Successfully generated setup.txt in your file manager!")
        
        # 4. Trigger an immediate git pull / sync check if setup.txt is already filled out
        try:
            import requests
            # We look at the file they just filled or an existing one
            if os.path.exists(setup_file_path):
                config = {}
                with open(setup_file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and "=" in line:
                            k, v = line.split("=", 1)
                            config[k.strip()] = v.strip()
                
                username = config.get("github_username")
                repo = config.get("github_repo")
                
                # If they already put their real info in, pull the files immediately!
                if username and username != "YOUR_USERNAME" and repo and repo != "YOUR_REPO_NAME":
                    print(f"🔄 [Mycord] Automatically pulling files from {username}/{repo}...")
                    api_url = f"https://api.github.com/repos/{username}/{repo}/git/trees/HEAD?recursive=1"
                    res = requests.get(api_url)
                    if res.status_code == 200:
                        data = res.json()
                        for item in data.get("tree", []):
                            if item.get("type") == "blob":
                                path = item["path"]
                                # Build folders and download files seamlessly
                                folder = os.path.dirname(path)
                                if folder:
                                    os.makedirs(folder, exist_ok=True)
                                raw_url = f"https://raw.githubusercontent.com/{username}/{repo}/HEAD/{path}"
                                file_res = requests.get(raw_url)
                                if file_res.status_code == 200:
                                    with open(path, "wb") as file_out:
                                        file_out.write(file_res.content)
                        print("✅ [Mycord] Repository files synced perfectly via pip install!")
        except Exception as e:
            # Pass silently so the pip install doesn't crash if they don't have internet or haven't filled setup.txt yet
            print(f"⚠️ [Mycord Sync Note] Initial sync skipped or configured to run on startup: {e}")

# ==============================================================================
# 📋 STANDARD PYPI PACKAGE CONFIGURATION
# ==============================================================================
setup(
    name="mycord",
    version="1.1.2",
    description="The ultimate self-syncing Discord bot framework framework.",
    author="luffy",
    packages=["mycord"],  # Points to your inner folder containing __init__.py
    install_requires=[
        "discord.py",
        "requests",
    ],
    cmdclass={
        'install': CustomInstallCommand,  # Binds our automatic setup.txt logic to pip install
    },
)
