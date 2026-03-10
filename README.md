# 📅 Telegram Task Planner Bot
![Build Status](https://github.com/Tehhy/TelegramBotPlanner/actions/workflows/python-app.yml/badge.svg)

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
   
### 🧹 Development Tools
We use a modern toolchain to keep the code clean and consistent:
* **Pre-commit** — Framework for managing git hooks.
* **Ruff** — An extremely fast Python linter and code formatter.
* **Black** — The uncompromising code formatter.
* **Isort** — Proper sorting of imports.

## 🚀 Quick Start
### 1. Prerequisites
Ensure you have [Poetry](https://python-poetry.org/docs/#installation) installed on your system.
### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/Tehhy/TelegramBotPlanner.git
cd TelegramBotPlanner
poetry install
```

### 3. Environment Setup
Create a .env file in the root directory:
```bash 
TELEGRAM_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_google_gemini_api_key
```

### 4. Installing pre-commit hooks
To ensure code quality and formatting, install the git hooks:
```bash
poetry run pre-commit install
```
To run all checks manually:
```bash
poetry run pre-commit run --all-files
```

### 5. Running the Bot
Run the application using the module execution command:
```bash
poetry run python -m src.my_bot.run
```

### 6. Running tests
To run the automated test suite, use:
```bash
poetry run pytest
```
