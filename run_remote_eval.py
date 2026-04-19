import json
import os
import requests
import time
import argparse

ENDPOINT = "https://gemma4-coding-762452591869.us-central1.run.app/v1/chat/completions"
MODEL_ID = "gs://super-power-agents-model-cache/models/gemma4-coding-merged"

def run_eval(test_file, output_file):
    results = []
    
    # Load existing results to resume if possible
    judged_topics = set()
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            for line in f:
                try:
                    res = json.loads(line)
                    judged_topics.add(res["topic"])
                except:
                    pass

    with open(test_file, "r") as f:
        test_cases = [json.loads(line) for line in f]

    print(f"Starting evaluation of {len(test_cases)} cases from {test_file}...")

    with open(output_file, "a") as out_f:
        for item in test_cases:
            topic = item.get("topic", "N/A")
            if topic in judged_topics:
                print(f"Skipping {topic}")
                continue
                
            prompt = item["prompt"]
            print(f"Processing: {topic}...", end="", flush=True)
            
            data = {
                "model": MODEL_ID,
                "messages": [
                    {"role": "system", "content": "You are a senior software engineer. Provide idiomatic code and concise technical rationales."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1024,
                "temperature": 0.0
            }
            
            start_time = time.time()
            try:
                response = requests.post(ENDPOINT, json=data, timeout=120)
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    end_time = time.time()
                    
                    res_obj = {
                        "topic": topic,
                        "prompt": prompt,
                        "response": content,
                        "duration": end_time - start_time
                    }
                    results.append(res_obj)
                    out_f.write(json.dumps(res_obj) + "\n")
                    out_f.flush()
                    print(" DONE")
                else:
                    print(f" ERROR: {response.status_code} - {response.text}")
            except Exception as e:
                print(f" ERROR: {str(e)}")
            
            # Rate limit/Congestion control
            time.sleep(1)

    print(f"Evaluation complete. Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-file", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    
    run_eval(args.test_file, args.output)
