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
    """Generates the setup.txt file right where the user runs their bot."""
    # This grabs the actual folder where the user is running their script
    current_working_dir = os.getcwd()
    setup_file_path = os.path.join(current_working_dir, "setup.txt")

    if not os.path.exists(setup_file_path):
        with open(setup_file_path, "w", encoding="utf-8") as f:
            f.write(
                "github_username=YOUR_USERNAME\n"
                "github_repo=YOUR_REPO_NAME\n"
                "ignore_files=setup.txt,.env,data\n"
            )
        print("✨ [Mycord] Successfully generated setup.txt in your file manager!")
        print("👉 Please configure setup.txt and restart your server.")
        sys.exit(0) # Stop execution so they can fill it out
