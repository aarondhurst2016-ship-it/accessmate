"""
ai_chat.py - Simple AI chat module using OpenAI API (ChatGPT-like)
- Requires 'openai' Python package and an API key
- Set your API key in the OPENAI_API_KEY environment variable or pass as argument
"""
import os
import openai

# You can set your API key as an environment variable or pass it directly
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")

openai.api_key = OPENAI_API_KEY

def chat_with_gpt(prompt, model="gpt-3.5-turbo", temperature=0.7, max_tokens=256):
    """Send a prompt to OpenAI's chat model and return the response."""
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"[AI Error: {e}]"

if __name__ == "__main__":
    print("Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "quit":
            break
        reply = chat_with_gpt(user_input)
        print(f"AI: {reply}")
