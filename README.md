# mycord

A minimalist, dynamic wrapper framework for discord.py with built-in database management.

**mycord** simplifies Discord bot development by providing a lightweight abstraction layer over discord.py, featuring automatic cog loading, integrated SQLite database management, and utility tools.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Components](#core-components)
  - [MyBot](#mybot)
  - [DB](#db)
  - [Cog](#cog)
  - [Tools](#tools)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Requirements](#requirements)

---

## Installation

### Prerequisites
- Python 3.8+
- pip

### From Source

Clone the repository and install in development mode:

```bash
git clone https://github.com/amri4/mycord.git
cd mycord
pip install -e .
```

### Dependencies
- `discord.py>=2.0.0` - Discord API wrapper
- `python-dotenv>=1.0.0` - Environment variable management

---

## Quick Start

### Basic Bot Setup

Create a main bot file (e.g., `main.py`):

```python
from mycord import MyBot
import asyncio

# Initialize the bot
bot = MyBot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"{bot.user} is now running!")

async def main():
    # Load cogs from ./cogs directory
    await bot.autoload_cogs("./cogs")
    await bot.start("YOUR_DISCORD_TOKEN")

asyncio.run(main())
```

### Environment Setup

Create a `.env` file in your project root:

```
TOKEN=your_discord_bot_token_here
```

Or use a custom token variable name:

```python
bot.run_bot(token_env_name="DISCORD_TOKEN")
```

---

## Core Components

### MyBot

The main bot class extending `discord.ext.commands.Bot` with integrated database and utilities.

#### Features
- **Automatic environment loading** - Finds and loads `.env` files automatically
- **Integrated database** - Built-in SQLite database accessible from bot instance
- **Dynamic cog loading** - Automatically load all Python files from a directory
- **Database proxy** - Access database methods directly from bot instance
- **Token management** - Flexible token retrieval from environment variables

#### Constructor

```python
MyBot(command_prefix, db_name="mycord_data.db", **options)
```

**Parameters:**
- `command_prefix` (str): Prefix for bot commands (e.g., "!", ".")
- `db_name` (str): Name of SQLite database file. Default: `"mycord_data.db"`
- `**options`: Additional keyword arguments passed to `discord.ext.commands.Bot`

**Attributes:**
- `_db` - Internal database instance
- `tools` - Reference to the Tools utility class

#### Methods

##### `autoload_cogs(directory: str = "./cogs")`

Automatically scans a directory and loads all Python files as Discord cogs.

```python
await bot.autoload_cogs("./cogs")
```

**Parameters:**
- `directory` (str): Path to cogs directory. Default: `"./cogs"`

**Behavior:**
- Creates the directory if it doesn't exist
- Loads all `.py` files (except those starting with `_`)
- Prints success/failure messages to console
- Continues loading even if a cog fails

##### `get_env(key: str, default: str = None) -> str`

Retrieve environment variables.

```python
token = bot.get_env("TOKEN")
api_key = bot.get_env("API_KEY", default="default_key")
```

**Parameters:**
- `key` (str): Environment variable name
- `default` (str): Default value if key not found

**Returns:** Environment variable value or default

##### `run_bot(token_env_name: str = "TOKEN")`

Start the bot with automatic token retrieval.

```python
bot.run_bot()  # Uses TOKEN env var
bot.run_bot(token_env_name="DISCORD_TOKEN")  # Uses DISCORD_TOKEN env var
```

**Parameters:**
- `token_env_name` (str): Environment variable containing the token. Default: `"TOKEN"`

#### Database Proxy

Access database methods directly from the bot:

```python
bot.create_table("users", "id INTEGER PRIMARY KEY, name TEXT")
bot.insert("users", "id, name", (1, "Alice"))
user = bot.fetchone("users", "id = ?", (1,))
```

---

### DB

A SQLite database wrapper for simple data persistence.

#### Constructor

```python
DB(db_name="mycord_data.db")
```

**Parameters:**
- `db_name` (str): SQLite database filename

**Attributes:**
- `conn` - SQLite connection object
- `cursor` - SQLite cursor for executing queries

#### Methods

##### `create_table(name: str, columns: str)`

Create a new table.

```python
db.create_table("users", "id INTEGER PRIMARY KEY, name TEXT, age INTEGER")
```

##### `insert(table: str, columns: str, values: tuple)`

Insert a new row into a table.

```python
db.insert("users", "name, age", ("Alice", 30))
```

##### `insert_replace(table: str, columns: str, values: tuple)`

Insert a row, replacing if a unique constraint conflict occurs.

```python
db.insert_replace("users", "id, name, age", (1, "Alice", 31))
```

##### `fetchone(table: str, condition: str = None, values: tuple = ())`

Fetch a single row from a table.

```python
user = db.fetchone("users")
user = db.fetchone("users", "id = ?", (1,))
user = db.fetchone("users", "name = ? AND age > ?", ("Alice", 25))
```

**Parameters:**
- `table` (str): Table name
- `condition` (str): WHERE clause without "WHERE" keyword
- `values` (tuple): Parameterized query values

**Returns:** Tuple of row data or None if not found

##### `fetchall(table: str)`

Fetch all rows from a table.

```python
all_users = db.fetchall("users")
```

**Parameters:**
- `table` (str): Table name

**Returns:** List of tuples

##### `update(table: str, set_values: str, condition: str, values: tuple)`

Update rows in a table.

```python
db.update("users", "age = ?", "id = ?", (31, 1))
```

**Parameters:**
- `table` (str): Table name
- `set_values` (str): SET clause (e.g., "age = ?")
- `condition` (str): WHERE clause
- `values` (tuple): Parameterized values

##### `delete(table: str, condition: str, values: tuple)`

Delete rows from a table.

```python
db.delete("users", "id = ?", (1,))
```

##### `exists(table: str, condition: str, values: tuple) -> bool`

Check if a row exists in a table.

```python
if db.exists("users", "id = ?", (1,)):
    print("User exists!")
```

**Returns:** Boolean

##### `close()`

Close the database connection.

```python
db.close()
```

---

### Cog

A base class for Discord cogs with automatic module injection for easy access to discord.py and discord.ext.commands utilities.

#### Overview

When you create a Cog subclass, all non-private attributes from `discord` and `discord.ext.commands` are automatically injected into your cog's module, allowing you to use them without explicit imports.

#### Example

```python
from mycord import Cog

class MyCog(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="ping")
    async def ping_command(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

The `commands.command` decorator is automatically available without importing `discord.ext.commands`.

#### How It Works

The `__init_subclass__` hook injects module-level attributes:
- All public members from `discord` module
- All public members from `discord.ext.commands` module

This allows cleaner, more concise cog files.

---

### Tools

A utility class providing helper methods for common Discord bot operations.

#### Methods

##### `chance(percentage: float) -> bool`

Return True with the given probability (0-100).

```python
if Tools.chance(50):
    print("50% chance succeeded!")

if Tools.chance(10):
    print("Only 10% chance!")
```

**Parameters:**
- `percentage` (float): Probability as a percentage (0-100)

**Returns:** Boolean

##### `timestamp() -> str`

Get the current timestamp as a formatted string.

```python
current_time = Tools.timestamp()
print(current_time)  # Output: "2024-01-15 14:30:45"
```

**Returns:** String in format "YYYY-MM-DD HH:MM:SS"

---

## API Reference

### Imports

```python
from mycord import MyBot, DB, Cog, Tools
```

All classes are automatically injected into your main module's namespace, so you can use them directly after importing.

---

## Examples

### Complete Bot with Database

```python
import asyncio
from mycord import MyBot, DB

# Create bot
bot = MyBot(command_prefix="!", db_name="bot_data.db")

@bot.event
async def on_ready():
    print(f"{bot.user} logged in!")
    
    # Initialize database
    bot.create_table(
        "user_points",
        "user_id INTEGER PRIMARY KEY, points INTEGER DEFAULT 0"
    )

@bot.command(name="points")
async def get_points(ctx):
    user_id = ctx.author.id
    
    # Use database through bot instance
    result = bot.fetchone("user_points", "user_id = ?", (user_id,))
    
    if result:
        points = result[1]
        await ctx.send(f"You have {points} points!")
    else:
        await ctx.send("No data found!")

async def main():
    await bot.autoload_cogs("./cogs")
    await bot.start("YOUR_TOKEN")

asyncio.run(main())
```

### Creating a Cog with Commands

Create `cogs/moderation.py`:

```python
from mycord import Cog

class ModerationCog(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_member(self, ctx, member: Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention}")
    
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_member(self, ctx, member: Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention}")

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
```

### Using Tools

```python
from mycord import Tools

# Random chance
if Tools.chance(75):
    print("75% roll succeeded!")

# Logging with timestamps
log_message = f"[{Tools.timestamp()}] Bot started successfully"
```

---

## Requirements

| Package | Version | Purpose |
|---------|---------|---------|
| discord.py | >=2.0.0 | Discord API wrapper |
| python-dotenv | >=1.0.0 | Environment variable management |
| Python | >=3.8 | Runtime |

---

## License

MIT License - See LICENSE file for details

## Author

Created by [amri4](https://github.com/amri4)
