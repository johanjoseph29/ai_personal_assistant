import os
import datetime
import pytz
import dateparser
import pickle
import json
import re

from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage
from langchain.tools import tool

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

from simplegmail import Gmail


SCOPES = ["https://www.googleapis.com/auth/calendar"]
TIMEZONE = "Asia/Kolkata"
TOKEN_FILE = "token.pkl"



def get_google_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    return build("calendar", "v3", credentials=creds)

@tool
def create_calendar_event(event_text: str) -> str:
    """Create a Google Calendar event from natural language."""

    service = get_google_service()

    extraction_prompt = f"""
Extract only the date and time from this sentence.
Return only the date and time phrase.

Sentence: "{event_text}"
"""

    extraction = llm.invoke([HumanMessage(content=extraction_prompt)])
    datetime_phrase = extraction.content.strip()

    parsed_date = dateparser.parse(
        datetime_phrase,
        settings={
            "PREFER_DATES_FROM": "future",
            "RELATIVE_BASE": datetime.datetime.now()
        }
    )

    if not parsed_date:
        return "I couldn't understand the date/time."

    tz = pytz.timezone(TIMEZONE)
    parsed_date = tz.localize(parsed_date)
    end_time = parsed_date + datetime.timedelta(hours=1)

    title_prompt = f"""
Remove date and time words from this sentence.
Return only the event title.

Sentence: "{event_text}"
"""

    title_response = llm.invoke([HumanMessage(content=title_prompt)])
    event_title = title_response.content.strip()

    event = {
        "summary": event_title,
        "start": {
            "dateTime": parsed_date.isoformat(),
            "timeZone": TIMEZONE,
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": TIMEZONE,
        },
    }

    service.events().insert(calendarId="primary", body=event).execute()

    return f"{event_title} scheduled for {parsed_date.strftime('%d %b %Y at %I:%M %p')}"


@tool
def read_unread_emails(_: str = "") -> str:
    """
    List unread email subjects from last 2 days.
    """

    gmail = Gmail()
    messages = gmail.get_messages(query="is:unread newer_than:2d")

    if not messages:
        return "No unread emails from last 2 days."

    result = "Unread Emails:\n\n"

    for msg in messages[:5]:
        result += f"Subject: {msg.subject}\n"
        result += f"From: {msg.sender}\n"
        result += f"Date: {msg.date}\n"
        result += "-" * 40 + "\n"

    return result



@tool
def get_and_summarize_latest_email(_: str = "") -> str:
    """
    Retrieve most recent email and summarize it.
    """

    gmail = Gmail()
    messages = gmail.get_messages(query="newer_than:2d")

    if not messages:
        return "No recent emails found."

    latest = messages[0]

    subject = latest.subject
    sender = latest.sender
    date = latest.date
    body = latest.plain or latest.snippet

    if not body:
        return "Could not extract email body."

    summary_prompt = f"""
Summarize this email clearly in 4 lines:

{body}
"""

    summary = llm.invoke([HumanMessage(content=summary_prompt)])

    return f"""
Email Details:
Subject: {subject}
From: {sender}
Date: {date}

Email Content:
{body[:1500]}

Summary:
{summary.content}
"""


@tool
def send_email(input_text: str) -> str:
    """
    Send an email.
    Format:
    recipient | subject | message
    """

    try:
        recipient, subject, message = input_text.split("|")
        recipient = recipient.strip()
        subject = subject.strip()
        message = message.strip()
    except:
        return "Format should be: recipient | subject | message"

    gmail = Gmail()
    gmail.send_message(to=recipient, subject=subject, msg_plain=message)

    return f"Email sent to {recipient}"


llm = ChatOllama(
    model="llama3.2",
    temperature=0,
    streaming=False
)



tools = {
    "create_calendar_event": create_calendar_event,
    "read_unread_emails": read_unread_emails,
    "send_email": send_email,
    "get_and_summarize_latest_email": get_and_summarize_latest_email
}

SYSTEM_PROMPT = """
You are a strict AI tool router.

Available tools:
- create_calendar_event
- read_unread_emails
- send_email
- get_and_summarize_latest_email

If a tool is required, respond ONLY in valid JSON:

{
  "tool": "tool_name",
  "input": "tool_input"
}

No explanations.
No markdown.
"""

def run_agent(user_input):

    response = llm.invoke([
        HumanMessage(content=SYSTEM_PROMPT + "\nUser: " + user_input)
    ])

    content = response.content.strip()

    json_match = re.search(r'\{.*\}', content, re.DOTALL)

    if json_match:
        try:
            data = json.loads(json_match.group())
            tool_name = data.get("tool")
            tool_input = data.get("input")

            if tool_name in tools:
                if tool_input is None:
                    tool_input = ""
                return tools[tool_name].invoke(tool_input)

        except Exception as e:
            print("Tool error:", e)

    return content


print("AI Agent Running...")

while True:
    user_input = input("You: ")
    reply = run_agent(user_input)
    print("Agent:", reply)
