# Examples

## Minimal bot

```python
import mycord

TOKEN = mycord.os.getenv("TOKEN")
bot = mycord.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"✅ Bot online as {bot.user}")

bot.start(TOKEN)
```

## Bot with cogs

```python
import mycord

bot = mycord.Bot(command_prefix="!")

@bot.event
async def on_ready():
    await bot.autoload_cogs()
    print("Cogs loaded")

bot.run_bot()
```

## Bot with database

```python
import mycord

bot = mycord.Bot(command_prefix="!")

@bot.event
async def on_ready():
    bot.create_table("users", "id INTEGER PRIMARY KEY, name TEXT")
    bot.insert_replace("users", "id, name", (1, "Alice"))
    user = bot.fetchone("users", "id = ?", (1,))
    print(user)

bot.run_bot()
```

## Cog file example

Create `cogs/general.py`:

```python
import mycord

class General(mycord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send("Pong!")

async def setup(bot):
    await bot.add_cog(General(bot))
```

Then in your main script:

```python
import mycord

bot = mycord.Bot(command_prefix="!")

@bot.event
async def on_ready():
    await bot.autoload_cogs()
    print("Cogs are ready")

bot.run_bot()
```
