import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pathlib import Path
from dotenv import load_dotenv

from pathlib import Path

load_dotenv(Path(__file__).resolve().parent / ".env")
import os

print("API key loaded:", bool(os.getenv("GOOGLE_API_KEY")))
load_dotenv("fraud_agent\.venv")
from agent import root_agent
APP_NAME = "fraud_detection"
USER_ID = "analyst_001"
SESSION_ID = "investigation_001"
async def ask_agent(runner: Runner, question: str):
    """Send one message and inspect ADK events."""
    print(f"\nUSER: {question}")
    message = types.Content(role="user", parts=[types.Part(text=question)])
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID,new_message=message,):
        print(f"\nEVENT AUTHOR: {event.author}")
        print(f"EVENT AUTHOR: {event.author}")
        for call in event.get_function_calls():
            print("TOOL CALL:", call.name)
            print("ARGUMENTS:", call.args)

        for response in event.get_function_responses():
            print("TOOL RESPONSE:", response.response)
            
        if event.is_final_response():
            if event.content:
                for part in event.content.parts or []:
                    if part.text:
                        print("\nAGENT:", part.text)
async def main():
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    await ask_agent(
        runner,
        "Investigate transaction TX1002.",
    )

    await ask_agent(
        runner,
        "What was the risk score of that transaction?",
    )

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    print("\nFINAL SESSION STATE:")
    print(session.state if session else "Session not found")


if __name__ == "__main__":
    asyncio.run(main())
