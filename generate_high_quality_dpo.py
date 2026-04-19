import json
import os
import requests
import time

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def generate_pair(prompt):
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found")
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
The flaw should be something a Senior Engineer would catch but a junior might miss.
"""

    def get_response(system, user):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{
                "parts": [{"text": system + "\n\nPROMPT: " + user}]
            }],
            "generationConfig": {
                "temperature": 0.7,
            }
        }
        try:
            time.sleep(1)
            res = requests.post(url, json=payload, timeout=90)
            if res.status_code == 200:
                return res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            else:
                print(f"API Error: {res.status_code} - {res.text}")
                return None
        except Exception as e:
            print(f"Exception: {e}")
            return None

    print(f"Generating 'Chosen' for: {prompt[:50]}...")
    chosen = get_response(system_prompt_chosen, prompt)
    if not chosen: return None

    print(f"Generating 'Rejected' for: {prompt[:50]}...")
    rejected = get_response(system_prompt_rejected, prompt)
    if not rejected: return None

    return {
        "prompt": prompt,
        "chosen": chosen,
        "rejected": rejected
    }

if __name__ == "__main__":
    with open("prompts_for_dpo.txt", "r") as f:
        prompts = [line.strip() for line in f if line.strip()]

    output_file = "dpo_data_fixed.jsonl"
    count = 0
    for p in prompts:
        pair = generate_pair(p)
        if pair:
            with open(output_file, "a") as out_f:
                out_f.write(json.dumps(pair) + "\n")
            count += 1
            print(f"Saved pair {count}")
        if count >= 20:
            break
