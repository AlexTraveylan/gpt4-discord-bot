
# ChatGPT Discord Bot

## Sumary

- [Overview](#overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Features](#features)
- [License](#license)

## Overview

The ChatGPT Discord Bot is a versatile chatbot that allows you to have conversations with the GPT-3.5 (or GPT-4 when available) model by OpenAI within Discord threads. It supports a range of features, including predefined personalities (such as JakePy, a Python expert), and the ability to generate images using DALL-E.

Update GPT-4 is available, GPT-4-turbo-preview too

## Installation

To run this bot, ensure you have Python 3.11 installed on your system. Follow the steps below to set up a virtual environment (venv) and install the required dependencies:

1. **Clone the bot's GitHub repository using the following command:**
    ```bash
    git clone https://github.com/AlexTraveylan/gpt4-discord-bot
    ```
2. **Navigate to the project directory:**
    ```bash
    cd gpt4-discord-bot
    ```
3. **Create a virtual environment using Python 3.11:**
    ```bash
    python -m venv venv
    ```
4. **Activate the virtual environment:**
    - On Linux/macOS:
        ```bash
        source venv/bin/activate
        ```
    - On Windows (PowerShell): 
        ```bash
        .\venv\Scripts\Activate
        ```
5. **Install the required dependencies from the requirements.txt file:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

To ensure the bot works correctly, create a .env file at the project's root directory and provide the following information:

```env
PYTHONPATH=.
OPENAI_API_KEY="Your OpenAI token to use the OpenAI API"
DISCORD_BOT_TOKEN="Your Discord bot token"
DISCORD_CLIENT_ID="Your Discord user ID"
```

Make sure to obtain your OpenAI token by signing up on their website and creating an API key. For the Discord bot token, you'll need to create an application on the [Discord Developer Portal](https://discord.com/developers/applications) and generate a bot token under the "Bot" tab. Your Discord user ID can be obtained by enabling Developer Mode in Discord and copying your own user ID.

## Features

Key features of the ChatGPT Discord Bot include:

- Real-time conversation with the GPT-3.5 (or GPT-4 or GPT-4-turbo-preview) model.
- Support for predefined personalities with preconfigured prompts, such as JakePy, a Python expert who can assist with pytest.
- The ability to generate images using DALL-E (upcoming feature).

Feel free to contribute to the bot's development or open issues to report bugs or suggest improvements.

Enjoy engaging in conversations with the ChatGPT Discord Bot! 🤖✨

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please add a [pull request](https://github.com/AlexTraveylan/gpt4-discord-bot/pulls) for help.

[![Discord](https://img.shields.io/discord/896479981809049630?color=7289DA&logo=discord&logoColor=ffffff)](https://discord.gg/vqv2ATz) ![GitHub contributors](https://img.shields.io/github/contributors/AlexTraveylan/gpt4-discord-bot.svg)