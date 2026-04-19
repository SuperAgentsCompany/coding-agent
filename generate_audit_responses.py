import requests
import json
import time
import os

ENDPOINT = "https://gemma4-coding-762452591869.asia-southeast1.run.app/v1/chat/completions"
MODEL_ID = "gs://super-power-agents-model-cache/models/gemma4-coding-merged"

def run_remote_audit():
    prompts = []
    with open("agentic_test_suite.jsonl", "r") as f:
        for line in f:
            prompts.append(json.loads(line))

    # Load existing results to skip
    existing_topics = set()
    if os.path.exists("audit_results.jsonl"):
        with open("audit_results.jsonl", "r") as f:
            for line in f:
                try:
                    res = json.loads(line)
                    existing_topics.add(res["topic"])
                except:
                    pass

    print(f"Starting audit generation for {len(prompts)} cases...")
    
    for p in prompts:
        topic = p["topic"]
        if topic in existing_topics:
            print(f"Skipping already processed topic: {topic}")
            continue

        prompt = p["prompt"]
        print(f"\nProcessing: {topic}")
        
        payload = {
            "model": MODEL_ID,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a senior software engineer. Provide idiomatic code and concise technical rationales. Follow all instructions precisely."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.0,
            "max_tokens": 1024
        }
        
        success = False
        retries = 3
        for i in range(retries):
            start_time = time.time()
            try:
                response = requests.post(ENDPOINT, json=payload, timeout=180) # Increased timeout
                response.raise_for_status()
                data = response.json()
                content = data['choices'][0]['message']['content']
                duration = time.time() - start_time
                
                result = {
                    "topic": topic,
                    "prompt": prompt,
                    "response": content,
                    "duration": duration,
                    "tokens": data.get("usage", {}).get("total_tokens", 0)
                }
                
                with open("audit_results.jsonl", "a") as f:
                    f.write(json.dumps(result) + "\n")
                
                print(f"Success. Duration: {duration:.2f}s")
                success = True
                break
            except Exception as e:
                print(f"Attempt {i+1} failed: {e}")
                time.sleep(5)
        
        if not success:
            print(f"Failed to process {topic} after {retries} retries.")
            
    print(f"\nAudit results updated in audit_results.jsonl")

if __name__ == "__main__":
    run_remote_audit()
