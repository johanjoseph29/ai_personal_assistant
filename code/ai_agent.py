import os
import datetime
import pytz
import dateparser
import pickle
import asyncio

from browser_use import Agent as BrowserAgent
from browser_use import Browser
from browser_use import ChatOllama as BrowserChatOllama


from langchain_ollama import ChatOllama as LCChatOllama
from langchain.messages import HumanMessage
from langchain.tools import tool
from langchain.agents import create_agent


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



main_llm = LCChatOllama(
    model="qwen2.5:7b",
    temperature=0,
)



@tool
def create_calendar_event(event_text: str) -> str:
    """Create a Google Calendar event from natural language."""

    service = get_google_service()

    extraction_prompt = f"""
Extract only the date and time from this sentence.
Return only the date and time phrase.

Sentence: "{event_text}"
"""

    extraction = main_llm.invoke([HumanMessage(content=extraction_prompt)])
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

    title_response = main_llm.invoke([HumanMessage(content=title_prompt)])
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
    """List unread email subjects from last 2 days."""

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
    """Retrieve most recent email and summarize it."""

    gmail = Gmail()
    messages = gmail.get_messages(query="newer_than:2d")

    if not messages:
        return "No recent emails found."

    latest = messages[0]

    subject = latest.subject
    sender = latest.sender
    date = latest.date
    body = latest.plain or latest.snippet

    summary_prompt = f"""
Summarize this email clearly (max 10 lines):

{body}
"""

    summary = main_llm.invoke([HumanMessage(content=summary_prompt)])

    return f"""
Email Details:
Subject: {subject}
From: {sender}
Date: {date}

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




@tool
async def browser_use(task: str) -> str:
    """Use browser to automate web tasks."""

    browser = Browser()

    browser_llm = BrowserChatOllama(
        model="qwen2.5:7b",
    )

    strict_task = f"""
STRICT EXECUTION MODE.

You MUST only perform the task below.
You are NOT allowed to:
- Visit unrelated websites
- Search random topics
- Compare products unless explicitly asked
- Navigate to Wikipedia
- Change the goal
- Perform additional research
- Take screenshots unless requested

If something fails, retry the SAME task.
Do not invent new goals.

USER TASK:
{task}

Stop immediately after completing the task.
Return a short summary of actions performed.
"""

    browser_agent = BrowserAgent(
        task=strict_task,
        llm=browser_llm,
        browser=browser,
        max_steps=20
    )

    result = await browser_agent.run()

    await browser.close()

    return str(result)




tool_list = [
    create_calendar_event,
    read_unread_emails,
    get_and_summarize_latest_email,
    send_email,
    browser_use
]

agent = create_agent(
    model=main_llm,
    tools=tool_list,
    system_prompt="You are a helpful assistant. Use tools only when necessary and follow user instructions strictly."
)


async def run_agent(user_input):
    response = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": user_input}
        ]
    })

    if "output" in response:
        return response["output"]

    return response["messages"][-1].content



async def main():
    print("AI Agent Running...")

    while True:
        user_input = input("You: ")
        reply = await run_agent(user_input)
        print("Agent:", reply)


if __name__ == "__main__":
    asyncio.run(main())
