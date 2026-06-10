# Getting Started

`mycord` is designed to make Discord bot setup simple.

## Create your bot

Create `main.py` with the following content:

```python
import mycord

TOKEN = mycord.os.getenv("TOKEN")

bot = mycord.Bot(command_prefix="e!")

@bot.event
async def on_ready():
    print(f"✅ Bot online as {bot.user}")

bot.start(TOKEN)
```

## Run the bot

Start your bot with:

```bash
python main.py
```

## Use `.env` directly

`mycord.Bot` automatically loads `.env` values on initialization. You can also start the bot with a named environment key:

```python
bot.run_bot(token_env_name="MY_TOKEN")
```

If you want to read environment values manually:

```python
token = bot.get_env("TOKEN", default="")
```
