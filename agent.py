import json
from urllib.request import Request, urlopen
from urllib.error import URLError

MODEL = "qwen2.5:3b"
API_URL = "http://localhost:11434/api/chat"

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant. Answer clearly and say when you are unsure.",
    }
]

print("Local chat started. Type 'exit' to stop.")

while True:
    user_text = input("\nUser: ").strip()

    if user_text.lower() in {"exit", "quit"}:
        break

    if not user_text:
        continue

    messages.append({"role": "user", "content": user_text})

    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "stream": False,
    }).encode("utf-8")

    request = Request(
        API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
    except URLError as error:
        print("Could not reach Ollama. Check that it is running and the model is downloaded.")
        print(error)
        break

    answer = result["message"]["content"]
    print(f"Assistant: {answer}")
    messages.append({"role": "assistant", "content": answer})