import sys
import os
import json
from openai import OpenAI
from pathlib import Path

def load_session_history(session_file):
    if session_file.exists():
        with session_file.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_session_history(session_file, messages):
    with session_file.open("w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)

def stream_response(response):
    try:
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print()
    except Exception as e:
        print(f"Error during streaming: {e}")

def get_embedding(client, text, model="text-embedding-3-small"):
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python chat.py [model=\"MODEL\"] [session=\"NAME\"] [stream=True] [show_embedding=True] \"prompt\"")
        sys.exit(1)

    model = "gpt-3.5-turbo"     # Select model. Default="gpt-3.5-turbo"
    max_tokens = 300            # Select max_tokens. Default=300.
    temperature = 1.0
    stream = True               # Change this to False if you want to wait for the entire generation to finish.
    show_embedding = False      # (Default=False) Displaying embedding in the response.
    track_embedding = True      # (Default=True) Saving embedding's to your session json file.
    session_name = "default"    # Choose which session you are interacting with for saving conversation history.
    prompt_parts = []

    for arg in args:
        if arg.startswith("model="):
            model = arg.split("=", 1)[1].strip("\"'")
        elif arg.startswith("max_tokens="):
            max_tokens = int(arg.split("=", 1)[1])
        elif arg.startswith("temperature="):
            temperature = float(arg.split("=", 1)[1])
        elif arg.startswith("stream="):
            stream = arg.split("=", 1)[1].strip().lower() == "true"
        elif arg.startswith("session="):
            session_name = arg.split("=", 1)[1].strip("\"'")
        elif arg.startswith("show_embedding="):
            show_embedding = arg.split("=", 1)[1].strip().lower() == "true"
        elif arg.startswith("track_embedding="):
            track_embedding = arg.split("=", 1)[1].strip().lower() == "true"
        else:
            prompt_parts.append(arg)

    if not prompt_parts:
        print("Error: Missing prompt.")
        sys.exit(1)

    prompt = " ".join(prompt_parts)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # Session management
    session_dir = Path("sessions")
    session_dir.mkdir(exist_ok=True)
    session_file = session_dir / f"{session_name}.json"
    messages = load_session_history(session_file)

    # Generate and attach embedding to the user message
    user_message = {"role": "user", "content": prompt}
    if track_embedding:
        embedding = get_embedding(client, prompt)
        user_message["embedding"] = embedding
        if show_embedding:
            print(f"\n[embedding: {len(embedding)} dims]")
            print(f"{embedding[:5]} ...\n")

    messages.append(user_message)

    if show_embedding:
        if track_embedding:
            print(f"\n[embedding: {len(embedding)} dims]")
            print(f"{embedding[:5]} ...\n")
        else:
            print("\n[Note: show_embedding=True but embedding was not generated due to track_embedding=False]\n")


    try:
        if stream:
            response = client.chat.completions.create(
                model=model,
                messages=[m for m in messages if "role" in m and "content" in m],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            print(f"[{model} | session: {session_name} | stream: on]")
            print("Assistant:", end=" ", flush=True)
            stream_response(response)

            # Re-fetch full response for saving
            full = client.chat.completions.create(
                model=model,
                messages=[m for m in messages if "role" in m and "content" in m],
                temperature=temperature,
                max_tokens=max_tokens
            )
            assistant_message = full.choices[0].message
        else:
            response = client.chat.completions.create(
                model=model,
                messages=[m for m in messages if "role" in m and "content" in m],
                temperature=temperature,
                max_tokens=max_tokens
            )
            assistant_message = response.choices[0].message
            print(f"[{model} | session: {session_name} | stream: off]")
            print("Assistant:", assistant_message.content.strip())

        messages.append(dict(assistant_message))
        save_session_history(session_file, messages)

    except Exception as e:
        print(f"OpenAI API returned an error:\n{e}")

if __name__ == "__main__":
    main()
