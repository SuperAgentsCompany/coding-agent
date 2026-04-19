import os
import json
import requests
import argparse
import time

def format_prompt(content):
    return f"<start_of_turn>user\n{content}<end_of_turn>\n<start_of_turn>model\n"

def run_local(prompts, model_name="gemma4-coding-adapter"):
    import torch
    from unsloth import FastLanguageModel
    max_seq_length = 1024
    dtype = None
    load_in_4bit = True

    print(f"Loading local model and adapter: {model_name}...", flush=True)
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = model_name,
        max_seq_length = max_seq_length,
        dtype = dtype,
        load_in_4bit = load_in_4bit,
    )
    FastLanguageModel.for_inference(model)

    results = []
    for prompt in prompts:
        print(f"\nPROMPT: {prompt}", flush=True)
        start_time = time.time()
        inputs = tokenizer(text=[format_prompt(prompt)], return_tensors="pt").to("cuda")
        outputs = model.generate(**inputs, max_new_tokens=512, use_cache=True)
        response = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        end_time = time.time()
        
        if "model\n" in response:
            response = response.split("model\n")[-1]
        
        results.append({
            "prompt": prompt,
            "response": response,
            "duration": end_time - start_time
        })
        print(f"RESPONSE:\n{response}", flush=True)
        print("-" * 50, flush=True)
    return results

def run_remote(prompts, endpoint, model="coding"):
    print(f"Calling remote endpoint: {endpoint} (model: {model})...", flush=True)
    results = []
    for prompt in prompts:
        print(f"\nPROMPT: {prompt}", flush=True)
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512,
            "temperature": 0.0
        }
        start_time = time.time()
        try:
            response = requests.post(f"{endpoint}/chat/completions", json=data, timeout=120)
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                end_time = time.time()
                results.append({
                    "prompt": prompt,
                    "response": content,
                    "duration": end_time - start_time
                })
                print(f"RESPONSE:\n{content}", flush=True)
            else:
                print(f"API Error: {response.text}", flush=True)
        except Exception as e:
            print(f"Connection Error: {str(e)}", flush=True)
        print("-" * 50, flush=True)
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", help="Remote API base URL (e.g., https://.../v1)")
    parser.add_argument("--model", default="coding", help="Model name for API")
    parser.add_argument("--local-model", default="gemma4-coding-adapter", help="Local model/adapter name")
    parser.add_argument("--test-file", default="agentic_test_suite.jsonl", help="Test suite file")
    args = parser.parse_known_args()[0]

    test_prompts = []
    if os.path.exists(args.test_file):
        with open(args.test_file, 'r') as f:
            for line in f:
                data = json.loads(line)
                test_prompts.append(data["prompt"])
    else:
        test_prompts = [
            "Write a Python function to find the longest common subsequence of two strings using dynamic programming.",
            "Explain how to use TypeScript's 'infer' keyword within a conditional type with an example.",
            "Search for all files containing 'TODO' in the current directory and its subdirectories using a shell command."
        ]

    print("\n=== STARTING EVALUATION ===", flush=True)
    if args.api:
        run_remote(test_prompts, args.api, args.model)
    else:
        run_local(test_prompts, args.local_model)
