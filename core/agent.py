import os
import json
import openai
from dotenv import load_dotenv
from core.memory import get_last_n

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in the environment")
openai.api_key = api_key

with open("core/kairos.json", encoding="utf-8") as f:
    archetype = json.load(f)

def generate_response(message: str) -> str:
    history = get_last_n()
    context = "".join([f"User: {user}\nKairos: {reply}\n" for user, reply in history])

    prompt = (
        f"Axioms:\n{chr(10).join(archetype['axioms'])}\n\n"
        f"Style: {archetype['style']}\n\n"
        f"Intent: {archetype['intent']}\n\n"
        f"{context}"
        f"User: {message}\nKairos:"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    return response['choices'][0]['message']['content'].strip()
