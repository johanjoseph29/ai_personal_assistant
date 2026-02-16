# Personal AI Assistant

Local LLM + Gmail API + Google Calendar API

A local AI-powered personal assistant built using LangChain and Ollama.

This assistant can: - Read unread emails - Retrieve and summarize the
latest email - Send emails - Create Google Calendar events using natural
language - Automatically route tasks using a strict JSON-based tool
system

The assistant runs locally using Ollama (llama3.2 model) and integrates
with Google services for real productivity automation.

------------------------------------------------------------------------

# Features

## Email Management

-   List unread emails from last 2 days
-   Retrieve latest email
-   Summarize email content using local LLM
-   Send emails using structured input format

## Calendar Management

-   Create events using natural language
-   Automatically extract date and time
-   Automatically extract event title

## Intelligent Tool Routing

-   Strict JSON-based routing
-   LLM decides which tool to call
-   Safe JSON parsing before execution
-   Robust handling of null inputs

## Fully Local AI Brain

-   Uses Ollama (llama3.2)
-   No OpenAI API required
-   Works offline except Google API calls

------------------------------------------------------------------------

# Tech Stack

-   Python 3.10+
-   LangChain
-   Ollama
-   SimpleGmail
-   Google Calendar API
-   Dateparser
-   Pytz

------------------------------------------------------------------------

# Installation & Setup Guide

## 1. Install Python

Ensure Python 3.10 or above is installed.

``` bash
python --version
```

------------------------------------------------------------------------

## 2. Download or Clone the Project

If using Git:

``` bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

Or manually download the project as a ZIP file and extract it.

------------------------------------------------------------------------

## 3. Install Required Python Packages

``` bash
pip install langchain langchain-ollama simplegmail google-api-python-client google-auth google-auth-oauthlib dateparser pytz
```

------------------------------------------------------------------------

## 4. Install Ollama

Download Ollama from:

https://ollama.com

After installing, pull the required model:

``` bash
ollama pull llama3.2
```

Start Ollama server:

``` bash
ollama serve
```

Keep this terminal running.

------------------------------------------------------------------------

# Google API Configuration

## 5. Create Google Cloud Project

1.  Go to https://console.cloud.google.com\
2.  Create a new project\
3.  Go to APIs & Services → Library\
4.  Enable:
    -   Google Calendar API\
    -   Gmail API

------------------------------------------------------------------------

## 6. Create OAuth Credentials

1.  Go to APIs & Services → Credentials\
2.  Click "Create Credentials"\
3.  Select "OAuth Client ID"\
4.  Choose "Desktop App"\
5.  Download the JSON credentials file

------------------------------------------------------------------------

## 7. Prepare Credential Files

You need two copies of the downloaded JSON file.

Rename one copy to:

credentials.json

Rename another copy to:

client_secret.json

Place both files in the project root directory.

------------------------------------------------------------------------

## 8. First-Time Authentication

When running the assistant for the first time:

-   Browser will open for Google Calendar authentication
-   Browser will open for Gmail authentication

After successful login, these files will be generated automatically:

token.pkl\
gmail_token.json

These store your access tokens securely.

------------------------------------------------------------------------

# Running the Assistant

1.  Start Ollama:

``` bash
ollama serve
```

2.  In another terminal:

``` bash
python ai_personal_assistant.py
```

You should see:

AI Agent Running...

------------------------------------------------------------------------

# Example Commands

Check unread emails:

check my unread emails

Summarize latest email:

check my last email and summarize it

Send email:

send email to test@gmail.com \| Hello \| How are you?

Schedule event:

schedule gym tomorrow at 6am

------------------------------------------------------------------------

# Security

Do NOT commit these files:

credentials.json\
client_secret.json\
token.pkl\
gmail_token.json

Add to .gitignore:

credentials.json\
client_secret.json\
token.pkl\
gmail_token.json\
**pycache**/

------------------------------------------------------------------------

# Future Improvements

-   News API integration
-   Internship deadline extractor
-   Auto reminder creation
-   Google Drive integration
-   Telegram bot interface
-   Conversation memory
-   Multi-step reasoning agent
-   Email priority scoring
-   Task extraction from emails

------------------------------------------------------------------------

