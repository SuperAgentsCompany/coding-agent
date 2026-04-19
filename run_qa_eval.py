import torch
import os
import json
import time
from unsloth import FastLanguageModel

def format_prompt(content):
    return f"<start_of_turn>user\n{content}<end_of_turn>\n<start_of_turn>model\n"

def run_eval(test_file, model_name, output_file):
    max_seq_length = 2048
    dtype = None
    load_in_4bit = True

    print(f"Loading model and adapter: {model_name}...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = model_name,
        max_seq_length = max_seq_length,
        dtype = dtype,
        load_in_4bit = load_in_4bit,
    )
    FastLanguageModel.for_inference(model)

    results = []
    with open(test_file, "r") as f:
        for line in f:
            item = json.loads(line)
            prompt = item["prompt"]
            topic = item.get("topic", "N/A")
            
            print(f"Processing: {topic}")
            start_time = time.time()
            inputs = tokenizer(text=[format_prompt(prompt)], return_tensors="pt").to("cuda")
            outputs = model.generate(**inputs, max_new_tokens=1024, use_cache=True)
            response = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
            end_time = time.time()
            
            if "model\n" in response:
                response = response.split("model\n")[-1]
            
            results.append({
                "topic": topic,
                "prompt": prompt,
                "response": response,
                "duration": end_time - start_time
            })
            
            # Incremental save
            with open(output_file, "w") as out_f:
                for res in results:
                    out_f.write(json.dumps(res) + "\n")

    print(f"Evaluation complete. Results saved to {output_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-file", default="qa_test_suite.jsonl")
    parser.add_argument("--model", default="gemma4-coding-dpo-adapter", help="Local adapter directory")
    parser.add_argument("--output", default="qa_results_new.jsonl")
    args = parser.parse_args()
    
    run_eval(args.test_file, args.model, args.output)
