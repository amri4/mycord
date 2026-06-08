import os
import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
from .database import DB
from .tools import Tools

class MyBot(commands.Bot):
    def __init__(self, command_prefix, db_name="mycord_data.db", **options):
        intents = options.pop('intents', discord.Intents.default())
        intents.message_content = True
        
        super().__init__(command_prefix=command_prefix, intents=intents, **options)
        
        # Automatically locate and load the .env file
        load_dotenv(find_dotenv())
        
        self._db = DB(db_name)
        self.tools = Tools
        
    def __getattr__(self, name):
        """Allows direct database method execution from the bot instance."""
        try:
            return super().__getattr__(name)
        except AttributeError:
            if hasattr(self._db, name):
                return getattr(self._db, name)
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    async def autoload_cogs(self, directory: str = "./cogs"):
        """Dynamically scans a directory and loads all Python files as cogs."""
        if not os.path.exists(directory):
            os.makedirs(directory)
            return

        for filename in os.listdir(directory):
            if filename.endswith(".py") and not filename.startswith("_"):
                cog_path = f"{directory[2:].replace('/', '.')}.{filename[:-3]}"
                try:
                    await self.load_extension(cog_path)
                    print(f"[mycord] Successfully loaded cog: {filename}")
                except Exception as e:
                    print(f"[mycord] Failed to load cog {filename}: {e}")

    def get_env(self, key: str, default: str = None) -> str:
        return os.getenv(key, default)

    async def close(self):
        self._db.close()
        await super().close()

    def run_bot(self, token_env_name: str = "TOKEN"):
        token = self.get_env(token_env_name) or token_env_name
        self.run(token)

