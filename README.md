# 📅 Telegram Task Planner Bot
[![Python application and Tests](https://github.com/Tehhy/TelegramBotPlanner/actions/workflows/tests.yml/badge.svg)](https://github.com/Tehhy/TelegramBotPlanner/actions/workflows/tests.yml)

An intelligent task management assistant integrated with Gemini AI.

## Project overview
### 🛠 Tech Stack
* **Python 3.10+**
* **pyTelegramBotAPI** — Telegram Bot interaction.
* **Poetry** — Dependency management and virtual environments.
* **python-dotenv** — Secure environment variable handling.
* **Pytest** — Automated unit testing.

### 📂 Project Structure                                             
 ```bash                                                            
 src/my_bot/ — Core bot logic and handlers.                         
 tests/ — Unit tests for algorithms.                                
 pyproject.toml — Poetry configuration and dependencies.            
 .env — (Git-ignored) API keys and secrets.                         
 ```                                                                

### 🌟 Features                                                                 
* AI Assistance: Smart task planning and suggestions powered by Gemini.       
* Voice input via Telegram voice messages. (planned)                                   
* Audio output for AI responses. (planned)                                              
* Multi-language support for AI interactions. (planned)                                
* Web search capabilities for AI responses. (planned)                                  
* Integrated maps and route planning. (planned)                                     
* Integrated calendar API (Google/iOS). (planned)           
* Note-taking functionality. (planned)          
* AI response styles options. (planned)
   
## 🧹 Development Tools
We use a modern toolchain to keep the code clean and consistent:
* **Pre-commit** — Framework for managing git hooks.
* **Ruff** — An extremely fast Python linter and code formatter.
* **Black** — The uncompromising code formatter.
* **Isort** — Proper sorting of imports.

### 💡 Best Practices in this Project
* **Lazy Loading:** Heavy AI libraries (`google-generativeai`) are imported only when needed to save memory.
* **Centralized Logging:** All logs are managed in `run.py` to ensure consistent output format.
* **Defensive Programming:** Active checks for `user_id` and environment variables prevent runtime crashes.

## 🚀 Step-by-Step Setup Guide
### 1. Prerequisites
* Python 3.11+
* [Poetry] (https://python-poetry.org/docs/#installation) 
* A Google Cloud Project with the Generative Language API enabled.

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/Tehhy/TelegramBotPlanner.git
cd TelegramBotPlanner
poetry install
```

### 3. Obtaining API Keys

* Go to Google AI Studio.
* Create a new API Key for Gemini.
* Get your Telegram Bot Token from @BotFather.

### 4. Environment Setup
Create a .env file in the root directory:

TELEGRAM_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_google_gemini_api_key
DATABASE_URL=sqlite:///./test.db

### 5. Installing pre-commit hooks
To ensure code quality and formatting, install the git hooks:
```bash
poetry run pre-commit install
```
To run all checks manually:
```bash
poetry run pre-commit run --all-files
```

### 6. Running the Bot
Run the application using the module execution command:
```bash
poetry run python -m src.my_bot.run
```

### 7. Running tests
To run the automated test suite, use:
```bash
poetry run pytest
```

## ⚙️ Environment Variables

The following variables must be defined in your `.env` file or system environment. 

| Variable | Description | Required | Default |
| :--- | :--- | :---: | :--- |
| `TELEGRAM_TOKEN` | Unique bot token from [@BotFather](https://t.me/botfather). | Yes | - |
| `GEMINI_API_KEY` | API key from [Google AI Studio](https://aistudio.google.com/). | Yes | - |
| `DATABASE_URL` | SQLAlchemy connection string for the database. | Yes | `sqlite:///./test.db` |

## ❓ Troubleshooting & FAQ
Q: Bot fails with FileNotFoundError: logs/bot.log
A: Ensure you are running the bot from the project root. The run.py script will automatically try to create a logs/ folder if it's missing.

Q: Gemini AI returns an error or empty response.
A: Check if your GEMINI_API_KEY is valid and hasn't hit its rate limit. Check logs/bot.log for specific API error codes.

Q: ModuleNotFoundError: No module named 'my_bot'
A: Ensure you are using python -m src.my_bot.run or that your PYTHONPATH is set to ./src.

Q: High memory usage.
A: We use lazy imports for heavy AI libraries. However, keeping many active user_chats in memory can increase usage.