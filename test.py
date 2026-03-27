import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

try:
    models = client.models.list()
    for m in models:
        print(m.id)
except Exception as e:
    print("Error listing models:", e)
