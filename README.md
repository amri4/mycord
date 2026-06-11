# mycord

A minimalist Discord bot wrapper around `discord.py`.

`mycord` is designed for beginners:
- One import: `import mycord`
- Simple bot startup with `bot.start()`
- Automatic `.env` loading for `TOKEN`
- Built-in `bot.db` helper for SQLite
- Lightweight wrapper over `discord.py` commands and events

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

## Quick Start

Create a `.env` file in the same folder as `main.py`:

```env
TOKEN=your_discord_bot_token_here
```

Create `main.py`:

```python
import mycord

bot = mycord.Bot(prefix="!")

@bot.event
async def on_ready():
    print("✅ Bot online")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

bot.start()
```

Run:

```bash
python main.py
```

## `mycord.Bot`

```python
bot = mycord.Bot(prefix="!", db_name="mycord_data.db")
```

The main bot class. It is a lightweight wrapper around `discord.py` that exposes commands, events, and database helpers.

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `prefix` | `str` | `"!"` | Command prefix |
| `token` | `str` | `None` | Discord bot token; if omitted, `TOKEN` is loaded from `.env` or environment |
| `db_name` | `str` | `"mycord_data.db"` | SQLite filename |

### Methods

#### `bot.start(token=None)`

Start the bot. If `token` is omitted, `mycord` loads `TOKEN` automatically.

```python
bot.start()
```

#### `bot.run_bot(token_env_name="TOKEN")`

Alias for `bot.start()` that reads the token from an environment variable name.

```python
bot.run_bot()
```

#### `bot.get_env(key, default=None)`

Read any environment variable.

```python
token = bot.get_env("TOKEN")
```

## Events and Commands

### Events

Use `@bot.event` to register event handlers.

```python
@bot.event
async def on_ready():
    print("Bot online")

@bot.event
async def on_message(ctx):
    print(ctx.content)
```

### Commands

Use `@bot.command(name="...")` to register commands.

```python
@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello!")
```

## Database Helpers

`mycord` includes a lightweight SQLite wrapper available as `bot.db`.

```python
bot.create_table("users", "id INTEGER PRIMARY KEY, name TEXT")
```

Common methods available on `bot` and `bot.db`:
- `create_table(name, columns)`
- `insert(table, columns, values)`
- `insert_replace(table, columns, values)`
- `fetchone(table, condition=None, values=())`
- `fetchall(table)`
- `update(table, set_values, condition, values)`
- `delete(table, condition, values)`
- `exists(table, condition, values)`

## Utilities

### `mycord.Tools`

```python
if mycord.Tools.chance(25):
    print("1 in 4 chance")

print(mycord.Tools.timestamp())
```

### `mycord.os`

A shortcut to Python's standard `os` module.

```python
prefix = mycord.os.getenv("PREFIX", "!")
```

## Example: Bot with Database

```python
import mycord

bot = mycord.Bot()

@bot.event
async def on_ready():
    bot.create_table("points", "user_id INTEGER PRIMARY KEY, amount INTEGER DEFAULT 0")

@bot.command(name="points")
async def points(ctx):
    row = bot.fetchone("points", "user_id = ?", (ctx.author.id,))
    total = row[1] if row else 0
    await ctx.send(f"Points: {total}")

bot.start()
```

## Requirements

- Python `>=3.8`
- `discord.py>=2.0.0`
- `python-dotenv>=1.0.0`
