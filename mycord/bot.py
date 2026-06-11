import os
from typing import Any, Dict, Optional, Union

import discord
from discord.ext import commands
from dotenv import find_dotenv, load_dotenv

from .database import DB
from .tools import Tools

DEFAULT_INTENTS = discord.Intents.default()
DEFAULT_INTENTS.message_content = True


class Bot(commands.Bot):
    def __init__(
        self,
        prefix: str = "!",
        token: Optional[str] = None,
        db_name: str = "mycord_data.db",
        intents: Optional[Union[discord.Intents, int, Dict[str, bool]]] = None,
        **options: Any,
    ):
        load_dotenv(find_dotenv())

        self.prefix = prefix
        self.token = token or os.getenv("TOKEN")
        self._db = DB(db_name)
        self.db = self._db
        self.tools = Tools
        self.options = options

        if intents is None:
            intents = DEFAULT_INTENTS
        elif isinstance(intents, int):
            intents = discord.Intents(intents)
        elif isinstance(intents, dict):
            intents = discord.Intents.from_dict(intents)
        elif not isinstance(intents, discord.Intents):
            raise TypeError("intents must be discord.Intents, int, or dict")

        if not intents.message_content:
            intents.message_content = True

        super().__init__(command_prefix=prefix, intents=intents, **options)

    def get_env(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return os.getenv(key, default)

    def start(self, token: Optional[str] = None, token_env_name: str = "TOKEN") -> None:
        if token is None:
            token = self.token or self.get_env(token_env_name)

        if not token:
            raise RuntimeError(
                "Discord bot token is required. "
                "Pass it to bot.start(token), or set TOKEN in .env."
            )

        self.token = token
        super().run(token, reconnect=True)

    def run_bot(self, token_env_name: str = "TOKEN") -> None:
        return self.start(token_env_name=token_env_name)

    async def send_message(
        self,
        channel_id: Union[int, str],
        content: str,
        tts: bool = False,
    ) -> discord.Message:
        channel = self.get_channel(int(channel_id))
        if channel is None:
            channel = await self.fetch_channel(int(channel_id))
        return await channel.send(content, tts=tts)

    def create_table(self, name: str, columns: str) -> None:
        self.db.create_table(name, columns)

    def insert(self, table: str, columns: str, values: tuple) -> None:
        self.db.insert(table, columns, values)

    def insert_replace(self, table: str, columns: str, values: tuple) -> None:
        self.db.insert_replace(table, columns, values)

    def fetchone(self, table: str, condition: Optional[str] = None, values: tuple = ()):
        return self.db.fetchone(table, condition, values)

    def fetchall(self, table: str):
        return self.db.fetchall(table)

    def update(self, table: str, set_values: str, condition: str, values: tuple) -> None:
        self.db.update(table, set_values, condition, values)

    def delete(self, table: str, condition: str, values: tuple) -> None:
        self.db.delete(table, condition, values)

    def exists(self, table: str, condition: str, values: tuple) -> bool:
        return self.db.exists(table, condition, values)
