import requests
import json

ENDPOINT = "https://gemma4-coding-762452591869.asia-southeast1.run.app/v1/chat/completions"
MODEL_ID = "gs://super-power-agents-model-cache/models/gemma4-coding-merged"

payload = {
    "model": MODEL_ID,
    "messages": [
        {
            "role": "system",
            "content": "You are a senior software engineer. Provide idiomatic code and concise technical rationales."
        },
        {
            "role": "user",
            "content": "Write a TypeScript function to deeply merge two objects, handling arrays and nested objects."
        }
    ],
    "temperature": 0.1,
    "max_tokens": 1024
}

print(f"Testing endpoint: {ENDPOINT}")
try:
    response = requests.post(ENDPOINT, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()
    
    print("\n--- RESPONSE CONTENT ---")
    print(data['choices'][0]['message']['content'])
    
    if 'reasoning' in data['choices'][0]['message']:
        print("\n--- REASONING ---")
        print(data['choices'][0]['message']['reasoning'])
    else:
        print("\nNo separate reasoning field found in response.")

except Exception as e:
    print(f"Error testing endpoint: {e}")
