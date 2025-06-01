import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def call_llm(prompt: str, model="gpt-4", temperature=0.7) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return response.choices[0].message["content"].strip()