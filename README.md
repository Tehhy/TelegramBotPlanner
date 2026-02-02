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
* Voice input via Telegram voice messages.                                    
* Audio output for AI responses.                                              
* Multi-language support for AI interactions.                                 
* Web search capabilities for AI responses.                                   
* Integrated maps and route planning.                                         
* Integrated calendar API (Google/iOS).                                       ## 🚀 Quick Start
* Note-taking functionality.                                                  ### 1. Prerequisites
* AI response styles options. 
* Ensure you have [Poetry](https://python-poetry.org/docs/#installation) installed on your system.
   

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

### 4. Running the Bot
Run the application using the module execution command:
```bash
poetry run python -m src.my_bot.run
```

### 5. Running tests
To run the automated test suite, use:
```bash
poetry run pytest
```