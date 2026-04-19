import json
import os
import sys
import time
import requests
import argparse

def run_prompt(prompt, endpoint, model="coding"):
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.0
    }
    try:
        start_time = time.time()
        response = requests.post(f"{endpoint}/chat/completions", json=data, timeout=120)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            usage = result.get("usage", {})
            completion_tokens = usage.get("completion_tokens", 0)
            
            duration = end_time - start_time
            tps = completion_tokens / duration if duration > 0 else 0
            
            return {
                "response": content,
                "duration": duration,
                "tokens": completion_tokens,
                "tps": tps
            }
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error running prompt: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", default="qa_test_suite.jsonl", help="Test suite file")
    parser.add_argument("--output", default="benchmark_results.jsonl", help="Output file")
    parser.add_argument("--api", required=True, help="Remote API base URL")
    parser.add_argument("--model", default="coding", help="Model name")
    args = parser.parse_args()
    
    if not os.path.exists(args.suite):
        print(f"Error: {args.suite} not found.")
        sys.exit(1)
        
    test_cases = []
    with open(args.suite, "r") as f:
        for line in f:
            test_cases.append(json.loads(line))
            
    print(f"Starting benchmark for {len(test_cases)} cases on {args.api}...")
    
    results = []
    # Clear output file
    with open(args.output, "w") as f:
        pass

    for i, case in enumerate(test_cases):
        topic = case["topic"]
        prompt = case["prompt"]
        print(f"[{i+1}/{len(test_cases)}] Topic: {topic}")
        
        res_data = run_prompt(prompt, args.api, args.model)
        
        if res_data:
            result = {
                "topic": topic,
                "prompt": prompt,
                "response": res_data["response"],
                "duration": res_data["duration"],
                "tokens": res_data["tokens"],
                "tps": res_data["tps"]
            }
            results.append(result)
            with open(args.output, "a") as f:
                f.write(json.dumps(result) + "\n")
            print(f"  Completed in {res_data['duration']:.2f}s ({res_data['tps']:.2f} TPS)")
        else:
            print(f"  Failed to get response for topic: {topic}")
            
    print(f"\nBenchmark complete. Results saved to {args.output}")
