# Personal AI Assistant (Local LLM + Gmail + Google Calendar)

A local AI-powered personal assistant built using LangChain, Ollama, Gmail API, and Google Calendar API.

This assistant can:

- Read unread emails
- Retrieve and summarize the latest email
- Send emails
- Create Google Calendar events using natural language
- Automatically route tasks using a JSON-based tool selection system

The assistant runs locally using Ollama (llama3.2 model) and integrates with Google services for real productivity automation.

---

## Features

### Email Management
- List unread emails from the last 2 days
- Retrieve latest email content
- Summarize latest email using local LLM
- Send emails using structured natural language format

### Calendar Management
- Create events using natural language
  - Example: `schedule gym tomorrow at 6am`
- Automatically extracts date and time
- Automatically extracts event title

### Intelligent Tool Routing
- Strict JSON-based tool selection
- LLM decides which tool to call
- Robust JSON parsing for safe execution

### Fully Local AI Brain
- Uses Ollama (llama3.2)
- No OpenAI API required
- Works offline except for Google API calls

---

## Tech Stack

- Python 3.10+
- LangChain
- Ollama
- SimpleGmail
- Google Calendar API
- Dateparser
- Pytz

---

## Architecture Overview

1. User enters natural language input
2. Input is sent to local LLM
3. LLM decides if a tool is required
4. LLM outputs strict JSON:
   {
     "tool": "tool_name",
     "input": "tool_input"
   }
5. System parses JSON
6. Selected tool executes
7. Response returned to user

This ensures clear separation between reasoning (LLM) and execution (tools).

---

## Project Structure

