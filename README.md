# mycord

A minimalist, dynamic wrapper framework for [discord.py](https://github.com/Rapptz/discord.py) with built-in database management.

**mycord** simplifies Discord bot development by providing a lightweight abstraction layer over discord.py — featuring automatic cog loading, an integrated SQLite database, and utility helpers. Everything is accessible through a single `import mycord`.

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
  - [Bot](#bot)
  - [Cog](#cog)
  - [DB](#db)
  - [Tools](#tools)
- [Examples](#examples)
  - [Minimal bot](#minimal-bot)
  - [Bot with cogs](#bot-with-cogs)
  - [Bot with database](#bot-with-database)
  - [Cog file example](#cog-file-example)
- [Requirements](#requirements)

---

## Installation

```bash
pip install mycord
```

### From source

```bash
git clone https://github.com/amri4/mycord.git
cd mycord
pip install -e .
```

### Dependencies

| Package | Version |
|---|---|
| `discord.py` | `>=2.0.0` |
| `python-dotenv` | `>=1.0.0` |
| Python | `>=3.8` |

---

## Quick Start

**1. Create a `.env` file:**

```
TOKEN=your_discord_bot_token_here
```

**2. Create `main.py`:**

```python
import mycord

TOKEN = mycord.os.getenv("TOKEN")

bot = mycord.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"✅ Bot online as {bot.user}")

bot.start(TOKEN)
```

That's it. No `asyncio.run`, no extra imports, no boilerplate.

---

## API Reference

### Bot

```python
bot = mycord.Bot(command_prefix, db_name="mycord_data.db", **options)
```

The main bot class. Extends `discord.ext.commands.Bot` with:
- Automatic `.env` loading
- Integrated SQLite database (accessible directly on the bot)
- Help command removed by default
- Synchronous `start()` — no event loop boilerplate needed

#### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `command_prefix` | `str` | *required* | Command prefix, e.g. `"!"` |
| `db_name` | `str` | `"mycord_data.db"` | SQLite database filename |
| `**options` | | | Any extra kwargs passed to `discord.ext.commands.Bot` |

#### Methods

---

##### `bot.start(token)`

Start the bot. Synchronous and blocking — no `asyncio` needed.

```python
bot.start(TOKEN)
```

| Parameter | Type | Description |
|---|---|---|
| `token` | `str` | Your Discord bot token |

---

##### `bot.run_bot(token_env_name="TOKEN")`

Start the bot by reading the token from a `.env` variable.

```python
bot.run_bot()                        # reads TOKEN from .env
bot.run_bot(token_env_name="MY_BOT_TOKEN")  # reads MY_BOT_TOKEN from .env
```

---

##### `await bot.autoload_cogs(directory="./cogs", log="✅️{cog} cog loaded!")`

Scan a directory and load every `.py` file as a cog. Creates the directory automatically if it doesn't exist.

```python
@bot.event
async def on_ready():
    await bot.autoload_cogs()
    # or with a custom message:
    await bot.autoload_cogs("./cogs", log="{cog} is ready 🚀")
    # or with a callback:
    await bot.autoload_cogs("./cogs", log=lambda cog: print(f"[{cog}] loaded"))
    # or silent:
    await bot.autoload_cogs("./cogs", log=None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `directory` | `str` | `"./cogs"` | Path to the cogs folder |
| `log` | `str \| callable \| None` | `"✅️{cog} cog loaded!"` | Log message. Use `{cog}` as a placeholder for the cog name, pass a callable, or `None` for silence |

Files starting with `_` are ignored (useful for `__init__.py` or helper files).

---

##### `bot.get_env(key, default=None)`

Read an environment variable.

```python
token = bot.get_env("TOKEN")
prefix = bot.get_env("PREFIX", default="!")
```

---

#### Database Proxy

All `DB` methods are available directly on the bot instance:

```python
bot.create_table("users", "id INTEGER PRIMARY KEY, name TEXT")
bot.insert("users", "id, name", (1, "Alice"))
user = bot.fetchone("users", "id = ?", (1,))
```

See the [DB](#db) section for the full method list.

---

### Cog

A base class for Discord cogs. Automatically injects all public members of `discord` and `discord.ext.commands` into your cog's module — so you never need extra imports inside cog files.

```python
from mycord import Cog

class MyCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

`commands`, `discord`, `Embed`, `Member`, `app_commands`, and every other public discord.py symbol are available without any import inside the file.

---

### DB

A simple SQLite wrapper for persistent data storage.

```python
from mycord import DB

db = DB("mybot.db")
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `db_name` | `str` | `"mycord_data.db"` | SQLite file to create/connect to |

#### Methods

---

##### `db.create_table(name, columns)`

Create a table if it doesn't already exist.

```python
db.create_table("users", "id INTEGER PRIMARY KEY, name TEXT, points INTEGER DEFAULT 0")
```

---

##### `db.insert(table, columns, values)`

Insert a new row.

```python
db.insert("users", "id, name, points", (1, "Alice", 100))
```

---

##### `db.insert_replace(table, columns, values)`

Insert a row, replacing the existing one on unique constraint conflict.

```python
db.insert_replace("users", "id, name, points", (1, "Alice", 200))
```

---

##### `db.fetchone(table, condition=None, values=())`

Fetch a single matching row. Returns a `tuple` or `None`.

```python
user = db.fetchone("users")                              # first row
user = db.fetchone("users", "id = ?", (1,))              # by id
user = db.fetchone("users", "name = ? AND points > ?", ("Alice", 50))
```

---

##### `db.fetchall(table)`

Fetch all rows. Returns a list of tuples.

```python
all_users = db.fetchall("users")
```

---

##### `db.update(table, set_values, condition, values)`

Update matching rows.

```python
db.update("users", "points = ?", "id = ?", (300, 1))
```

---

##### `db.delete(table, condition, values)`

Delete matching rows.

```python
db.delete("users", "id = ?", (1,))
```

---

##### `db.exists(table, condition, values)`

Check if a matching row exists. Returns `bool`.

```python
if db.exists("users", "id = ?", (1,)):
    print("User found!")
```

---

##### `db.close()`

Close the database connection. Called automatically when the bot shuts down.

```python
db.close()
```

---

### Tools

A collection of static utility helpers.

```python
from mycord import Tools
# or via bot:
# bot.tools.chance(50)
```

---

##### `Tools.chance(percentage)`

Returns `True` with the given probability.

```python
if Tools.chance(25):
    print("1 in 4 chance hit!")
```

| Parameter | Type | Description |
|---|---|---|
| `percentage` | `float` | Probability from `0` to `100` |

**Returns:** `bool`

---

##### `Tools.timestamp()`

Returns the current time as a formatted string.

```python
now = Tools.timestamp()
print(now)  # "2024-06-09 14:30:45"
```

**Returns:** `str` — formatted as `"YYYY-MM-DD HH:MM:SS"`

---

## Examples

### Minimal bot

```python
import mycord

TOKEN = mycord.os.getenv("TOKEN")

bot = mycord.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"✅ Bot online as {bot.user}")

bot.start(TOKEN)
```

---

### Bot with cogs

`main.py`:

```python
import mycord

TOKEN = mycord.os.getenv("TOKEN")

bot = mycord.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"✅ Bot online as {bot.user}")
    await bot.autoload_cogs("./cogs", log="{cog} loaded ✅️")

bot.start(TOKEN)
```

`cogs/general.py`:

```python
from mycord import Cog

class General(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"🏓 Pong! `{round(self.bot.latency * 1000)}ms`")

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send(f"Hey {ctx.author.mention}! 👋")

async def setup(bot):
    await bot.add_cog(General(bot))
```

---

### Bot with database

```python
import mycord

TOKEN = mycord.os.getenv("TOKEN")

bot = mycord.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"✅ Bot online as {bot.user}")
    bot.create_table("points", "user_id INTEGER PRIMARY KEY, amount INTEGER DEFAULT 0")

@bot.command(name="points")
async def points(ctx):
    row = bot.fetchone("points", "user_id = ?", (ctx.author.id,))
    total = row[1] if row else 0
    await ctx.send(f"💰 You have **{total}** points.")

@bot.command(name="addpoints")
@commands.has_permissions(administrator=True)
async def addpoints(ctx, member: mycord.Member, amount: int):
    existing = bot.fetchone("points", "user_id = ?", (member.id,))
    if existing:
        bot.update("points", "amount = amount + ?", "user_id = ?", (amount, member.id))
    else:
        bot.insert("points", "user_id, amount", (member.id, amount))
    await ctx.send(f"✅ Added **{amount}** points to {member.mention}.")

bot.start(TOKEN)
```

---

### Cog file example

`cogs/moderation.py`:

```python
from mycord import Cog

class Moderation(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, *, reason="No reason provided"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 Kicked **{member}** — {reason}")

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, *, reason="No reason provided"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 Banned **{member}** — {reason}")

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"🧹 Cleared **{amount}** messages.")
        await msg.delete(delay=3)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
```

---

## Requirements

| Package | Version | Purpose |
|---|---|---|
| `discord.py` | `>=2.0.0` | Discord API wrapper |
| `python-dotenv` | `>=1.0.0` | Automatic `.env` loading |
| Python | `>=3.8` | Runtime |

---

## Author

Created by [amri4](https://github.com/amri4)

## License

MIT License — see [LICENSE](LICENSE) for details.
