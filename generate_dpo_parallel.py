import json
import os
import requests
import time
import sys

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def generate_pair(prompt):
    if not GEMINI_API_KEY:
        return None

    system_prompt_chosen = """
You are a Senior Software Engineer. Provide a high-quality, professional, and concise response to the user's coding prompt.
- Ensure correctness and idiomaticity.
- Follow all constraints strictly.
- Use tools correctly if implied.
- Include validation steps (e.g., tests, syntax checks).
- No unnecessary chitchat.
"""

    system_prompt_rejected = """
You are an AI assistant that provides slightly flawed coding advice.
Provide a response that looks professional but contains a subtle, critical flaw:
- Hallucinate a tool argument or name.
- Use a legacy or non-idiomatic pattern (e.g., manual loop instead of vectorization, acquire/release instead of context manager).
- Ignore one specific constraint from the prompt.
- Skip crucial validation or error handling.
- Be overly verbose with low-signal explanations.
"""

    def get_response(system, user):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{
                "parts": [{"text": system + "\n\nPROMPT: " + user}]
            }],
            "generationConfig": {
                "temperature": 0.7,
            }
        }
        try:
            print(f"Calling Gemini API for {url}...", file=sys.stderr)
            res = requests.post(url, json=payload, timeout=90)
            if res.status_code == 200:
                print("API Success", file=sys.stderr)
                return res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            else:
                print(f"API Error: {res.status_code} - {res.text}", file=sys.stderr)
                return None
        except Exception as e:
            print(f"Exception: {e}", file=sys.stderr)
            return None

    chosen = get_response(system_prompt_chosen, prompt)
    if not chosen: return None
    rejected = get_response(system_prompt_rejected, prompt)
    if not rejected: return None

    return {"prompt": prompt, "chosen": chosen, "rejected": rejected}

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(input_file, "r") as f:
        prompts = [line.strip() for line in f if line.strip()]

    for p in prompts:
        pair = generate_pair(p)
        if pair:
            with open(output_file, "a") as out_f:
                out_f.write(json.dumps(pair) + "\n")
            print(f"[{input_file}] Saved pair")
        time.sleep(2)
