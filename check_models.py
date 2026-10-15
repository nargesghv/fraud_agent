import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv(Path(__file__).resolve().parent / ".env")

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

for model in client.models.list():
    print(model.name)