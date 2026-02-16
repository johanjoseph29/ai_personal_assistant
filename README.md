# Personal AI Assistant

### Local LLM + Gmail API + Google Calendar API

A powerful local AI-powered personal assistant built using **LangChain
Tools**, `create_agent`, and **Ollama**.

This assistant can:

-   📧 Read unread emails\
-   📝 Retrieve and summarize the latest email\
-   📤 Send emails\
-   📅 Create Google Calendar events using natural language\
-   🌐 Perform web scraping and automated web-based tasks\
-   🧠 Automatically route tasks using LangChain `@tool` decorators and
    `create_agent`

The assistant runs locally using **Ollama** and integrates with Google
services for real productivity automation.

------------------------------------------------------------------------

# 🚀 Features

## 📬 Email Management

-   List unread emails from last 2 days\
-   Retrieve latest email\
-   Summarize email content using local LLM\
-   Send emails using structured input format

## 📅 Calendar Management

-   Create events using natural language\
-   Automatically extract date and time\
-   Automatically extract event title

## 🌐 Web Scraping & Automation

-   Scrape web data\
-   Perform automated browser tasks\
-   Extract information from websites\
-   Automate repetitive web-based workflows

## 🧠 Intelligent Tool Routing (LangChain)

-   Uses LangChain `@tool` decorator for tool definitions\
-   Uses `create_agent()` for structured agent creation\
-   LLM automatically decides which tool to invoke\
-   Clean separation between reasoning and execution\
-   Async support for browser automation\
-   Robust handling of null inputs

------------------------------------------------------------------------

# 💻 Fully Local AI Brain

-   Uses Ollama models (e.g., `qwen2.5`, `llama3.2`)\
-   No OpenAI API required\
-   Works offline except Google API calls

------------------------------------------------------------------------

# ⚠ Model Recommendation for Browser Automation

For reliable browser automation and multi-step web interaction, it is
**strongly recommended to use higher-parameter models (13B or above)**
with `browser_use`.

Smaller local models (such as `qwen2.5:7b`) may struggle with:

-   Long-horizon planning\
-   Dynamic page interaction\
-   Multi-step navigation\
-   DOM reasoning

However, the following tasks work efficiently with `qwen2.5` or similar
7B models:

-   ✅ Email management\
-   ✅ Calendar event creation\
-   ✅ Email summarization\
-   ✅ General reasoning\
-   ✅ Tool routing via LangChain

------------------------------------------------------------------------

# 🏗 Architecture Overview

1.  User enters natural language input.\
2.  Input is sent to local LLM (via LangChain).\
3.  `create_agent()` manages tool routing.\
4.  If required, the agent selects a tool defined using `@tool`.\
5.  The selected tool executes safely.\
6.  The result is returned to the user.

This ensures clean separation between:

-   🧠 Reasoning (LLM via LangChain)\
-   ⚙ Execution (Tools)

------------------------------------------------------------------------

# 🛠 Tech Stack

-   Python 3.10+\
-   LangChain\
-   LangChain-Ollama\
-   Ollama\
-   SimpleGmail\
-   Google Calendar API\
-   Dateparser\
-   Pytz

------------------------------------------------------------------------

# ▶ Running the Assistant

Start Ollama:

``` bash
ollama serve
```

Run the assistant:

``` bash
python ai_personal_assistant.py
```

------------------------------------------------------------------------

# 🔒 Security

Do NOT commit:

-   credentials.json\
-   client_secret.json\
-   token.pkl\
-   gmail_token.json

Add to `.gitignore`:

    credentials.json
    client_secret.json
    token.pkl
    gmail_token.json
    __pycache__/
