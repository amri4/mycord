# Installation

Install `mycord` from PyPI:

```bash
pip install mycord
```

## Requirements

- Python 3.8+
- `discord.py>=2.0.0`
- `python-dotenv>=1.0.0`

These dependencies are installed automatically when you install `mycord`.

## Install from source

To work with the latest repository version:

```bash
git clone https://github.com/amri4/mycord.git
cd mycord
pip install -e .
```

## Optional setup

Create a `.env` file in the project root to store your Discord bot token and other environment values:

```text
TOKEN=your_discord_bot_token_here
PREFIX=!
```
