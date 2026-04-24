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
* Multilingual Support: Intelligent language detection and responses in 40+ languages.
* Voice input via Telegram voice messages. (planned)                                   
* Audio output for AI responses. (planned)                                               
* Web search capabilities for AI responses. (planned)                                  
* Integrated maps and route planning. (planned)                                     
* Integrated calendar API (Google/iOS). (planned)           
* Note-taking functionality. (planned)          
* AI response styles options. (planned)

## 🛠 AI Features & Usage

### 🌍 Language Support
The bot features native multilingual support powered by Gemini AI:
* **Auto-Detection:** Simply send a message in your language (Russian, English, Spanish, etc.), and the AI will detect it automatically.
* **Context Preservation:** The bot maintains the conversation in the language you started with.
* **Smart Fallback:** If the language is unclear, the bot defaults to English to ensure a response.

### 📝 Interaction Tips
* **Task Planning:** Ask the bot to "Organize my day" or "Create a workout schedule". It will provide structured, bullet-point plans.
* **Concise Responses:** The AI is instructed to be brief and actionable. 
* **Large Requests:** If a response exceeds Telegram's limits, the bot automatically splits the text into multiple messages to ensure no information is lost.

### 🤖 Commands
* `/start` — Initialize the bot and get a welcome message.
* **Direct Input** — Send any text or task description to get an AI-powered response.
   
## 🧹 Development Tools
* **Pre-commit** — Framework for managing git hooks.
* **Ruff** — An extremely fast Python linter and code formatter.
* **Mypy** for static type checking.

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

```env
TELEGRAM_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_google_gemini_api_key
DATABASE_URL=sqlite:///./test.db
```

### 5. Installing pre-commit hooks
To ensure code quality and formatting, install the git hooks:
```bash
poetry run pre-commit install
```
To run all checks manually:
```bash
poetry run pre-commit run --all-files
```
Or run specific tools directly via Poetry:
```bash
poetry run ruff check .    # Linting
poetry run ruff format .   # Formatting
poetry run mypy src        # Type checking
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