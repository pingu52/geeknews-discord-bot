# GeekNews Discord Bot

[한국어 README](README-ko.md)

This is a Discord bot that fetches the latest topics from GeekNews and posts updates in a designated Discord channel.

## Features

-   Automatically retrieves the latest topics from GeekNews.
-   Posts topic details in a specified Discord channel.
-   Periodically checks for new topics to keep users updated.

## Requirements

-   Python 3.8 or higher
-   `discord.py` library
-   Other required libraries in `requirements.txt`

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/geeknews-discord-bot.git
cd geeknews-discord-bot
```

2. **Install the dependencies**

```bash
pip install -r requirement.txt
```

3. **Set up environment variables**

-   Create a `.env` file and add your token.

```
DISCORD_TOKEN = your_discord_token
GUILD_ID = your_guild_id
CHANNEL_ID = your_chennel_id
```

4. **Run the bot**

```bash
python main.py
```

## Files

-   `main.py`: The main entry point for running the bot.
-   `discord_bot.py`: Contains the bot's functionality and commands for interacting with Discord.
-   `geeknews_check.py`: Contains the logic for scraping and retrieving the latest topics from GeekNews.

## Usage

1. Invite the bot to your Discord server.
2. The bot will automatically post updates in the specified channel whenever new topics are found.
