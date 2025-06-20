# llm_interface.py

from ollama import chat

def query_llm(prompt: str) -> str:
    try:
        stream = chat(
            model="tinyllama",  # or your pulled model
            messages=[{"role": "user", "content": prompt}],
            stream=False
        )
        return stream["message"]["content"]
    except Exception as e:
        print("[LLM ERROR]", e)
        return "I'm sorry, something went wrong with the assistant."

# print(query_llm("Hello"))