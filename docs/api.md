# API Reference

## `mycord.Bot`

`mycord.Bot` is the main bot class.
It extends `discord.ext.commands.Bot` and includes:

- automatic `.env` loading via `python-dotenv`
- an integrated SQLite database instance
- convenient cog autoloading
- `run_bot()` for environment-based startup

### Initialization

```python
bot = mycord.Bot(command_prefix, db_name="mycord_data.db", **options)
```

#### Parameters

- `command_prefix` (`str`): required command prefix.
- `db_name` (`str`): SQLite filename, default `mycord_data.db`.
- `**options`: passed directly to `discord.ext.commands.Bot`.

### Methods

#### `bot.start(token)`

Start the bot using a token string.

#### `bot.run_bot(token_env_name="TOKEN")`

Start the bot by reading a token from the environment.

```python
bot.run_bot()
bot.run_bot(token_env_name="MY_TOKEN")
```

#### `await bot.autoload_cogs(directory="./cogs")`

Load every `.py` file in a directory as a cog.

- skips files beginning with `_`
- creates the directory if it does not exist

```python
await bot.autoload_cogs()
```

#### `bot.get_env(key, default=None)`

Read an environment variable.

```python
db_name = bot.get_env("DB_NAME", default="mycord_data.db")
```

### Database proxy

All `mycord.DB` methods are available directly on the bot instance.

```python
bot.create_table("users", "id INTEGER PRIMARY KEY, name TEXT")
bot.insert("users", "id, name", (1, "Alice"))
user = bot.fetchone("users", "id = ?", (1,))
```

## `mycord.Cog`

A base class for cogs that injects public `discord` and `discord.ext.commands` symbols into the cog module.

```python
import mycord

class General(mycord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

async def setup(bot):
    await bot.add_cog(General(bot))
```

## `mycord.DB`

A lightweight SQLite wrapper.

```python
db = mycord.DB("mybot.db")
```

### Methods

- `create_table(name, columns)`
- `insert(table, columns, values)`
- `insert_replace(table, columns, values)`
- `fetchone(table, condition=None, values=())`
- `fetchall(table)`
- `update(table, set_values, condition, values)`
- `delete(table, condition, values)`
- `exists(table, condition, values)`
- `close()`

## `mycord.Tools`

Utility helpers.

### `Tools.chance(percentage)`

Return `True` with the provided chance.

### `Tools.timestamp()`

Return the current timestamp as a string.

## `mycord.os`

The package exposes the standard `os` module from `mycord.os`.

```python
from mycord import os
TOKEN = mycord.os.getenv("TOKEN")
```
