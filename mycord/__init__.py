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

