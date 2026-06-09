# mycord

A minimalist, dynamic wrapper framework for [discord.py](https://github.com/Rapptz/discord.py) with built-in database management.

**mycord** simplifies Discord bot development through a single import — `import mycord`. No scattered imports, no boilerplate. Everything lives under the `mycord` namespace.

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
  - [mycord.Bot](#mycordbot)
  - [mycord.Cog](#mycordcog)
  - [mycord.DB](#mycorddb)
  - [mycord.Tools](#mycordtools)
  - [mycord.os](#mycordos)
- [Examples](#examples)
  - [Minimal bot](#minimal-bot)
  - [Bot with cogs](#bot-with-cogs)
  - [Bot with database](#bot-with-database)
  - [Cog file example](#cog-file-example)
  - [Moderation cog](#moderation-cog)
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

That's it. One import. No `asyncio`, no scattered `from discord import ...`.

---

## API Reference

### `mycord.Bot`

```python
bot = mycord.Bot(command_prefix, db_name="mycord_data.db", **options)
```

The main bot class. Extends `discord.ext.commands.Bot` with:
- Automatic `.env` loading via `python-dotenv`
- Integrated SQLite database accessible directly on the bot instance
- Help command removed by default
- Synchronous `start()` — no event loop setup needed

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

---

##### `bot.run_bot(token_env_name="TOKEN")`

Start the bot by reading the token directly from `.env`.

```python
bot.run_bot()                              # reads TOKEN
bot.run_bot(token_env_name="MY_TOKEN")     # reads MY_TOKEN
```

---

##### `await bot.autoload_cogs(directory="./cogs", log="✅️{cog} cog loaded!")`

Scan a folder and load every `.py` file as a cog. Creates the folder if it doesn't exist. Files starting with `_` are skipped.

```python
@bot.event
async def on_ready():
    await bot.autoload_cogs()
    # custom message:
    await bot.autoload_cogs("./cogs", log="{cog} is ready 🚀")
    # callback:
    await bot.autoload_cogs("./cogs", log=lambda cog: print(f"[{cog}] online"))
    # silent:
    await bot.autoload_cogs("./cogs", log=None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `directory` | `str` | `"./cogs"` | Path to the cogs folder |
| `log` | `str \| callable \| None` | `"✅️{cog} cog loaded!"` | Use `{cog}` as a placeholder, pass a callable, or `None` for silence |

---

##### `bot.get_env(key, default=None)`

Read an environment variable.

```python
token = bot.get_env("TOKEN")
prefix = bot.get_env("PREFIX", default="!")
```

---

##### Database proxy

All `mycord.DB` methods are available directly on the bot instance:

```python
bot.create_table("users", "id INTEGER PRIMARY KEY, name TEXT")
bot.insert("users", "id, name", (1, "Alice"))
user = bot.fetchone("users", "id = ?", (1,))
```

See [`mycord.DB`](#mycorddb) for the full method list.

---

### `mycord.Cog`

Base class for Discord cogs. Automatically injects all public members of `discord` and `discord.ext.commands` into the cog's module — so `commands`, `Embed`, `Member`, `app_commands`, and every other discord.py symbol are available inside the file without any extra imports.

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

> `commands`, `Member`, `Embed`, `app_commands`, etc. are all injected automatically. No `from discord.ext import commands` needed.

---

### `mycord.DB`

A simple SQLite wrapper for persistent data storage.

```python
db = mycord.DB("mybot.db")
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `db_name` | `str` | `"mycord_data.db"` | SQLite file to create/open |

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

Insert a row, replacing the existing one on a unique constraint conflict.

```python
db.insert_replace("users", "id, name, points", (1, "Alice", 200))
```

---

##### `db.fetchone(table, condition=None, values=())`

Fetch a single matching row. Returns a `tuple` or `None`.

```python
user = db.fetchone("users")                                          # first row
user = db.fetchone("users", "id = ?", (1,))                          # by id
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

---

### `mycord.Tools`

Static utility helpers.

---

##### `mycord.Tools.chance(percentage)`

Returns `True` with the given probability.

```python
if mycord.Tools.chance(25):
    print("1 in 4 chance!")
```

| Parameter | Type | Description |
|---|---|---|
| `percentage` | `float` | Probability `0`–`100` |

**Returns:** `bool`

---

##### `mycord.Tools.timestamp()`

Returns the current time as a formatted string.

```python
now = mycord.Tools.timestamp()
print(now)  # "2024-06-09 14:30:45"
```

**Returns:** `str` — format: `"YYYY-MM-DD HH:MM:SS"`

---

### `mycord.os`

The standard library `os` module, available directly under `mycord` after your `.env` is auto-loaded. Useful for reading tokens and config.

```python
TOKEN = mycord.os.getenv("TOKEN")
prefix = mycord.os.getenv("PREFIX", "!")
```

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
import mycord

class General(mycord.Cog):
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

@bot.command(name="give")
@commands.has_permissions(administrator=True)
async def give(ctx, member: mycord.Member, amount: int):
    if bot.exists("points", "user_id = ?", (member.id,)):
        bot.update("points", "amount = amount + ?", "user_id = ?", (amount, member.id))
    else:
        bot.insert("points", "user_id, amount", (member.id, amount))
    await ctx.send(f"✅ Gave **{amount}** points to {member.mention}.")

bot.start(TOKEN)
```

---

### Cog file example

`cogs/general.py`:

```python
import mycord

class General(mycord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"🏓 `{round(self.bot.latency * 1000)}ms`")

    @commands.command(name="info")
    async def info(self, ctx, member: Member = None):
        member = member or ctx.author
        embed = Embed(title=str(member), color=member.color)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"))
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
```

---

### Moderation cog

`cogs/moderation.py`:

```python
import mycord

class Moderation(mycord.Cog):
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
