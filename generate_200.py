import subprocess
import json
import os
import re
import time
import sys

def extract_json_lines(text):
    if not text: return []
    lines = []
    # Use DOTALL to match across newlines
    potential_lines = re.findall(r'\{.*?"messages".*?\}', text, re.DOTALL)
    for line in potential_lines:
        try:
            # Load it to verify it's valid JSON
            data = json.loads(line)
            # Dump it back to a single line for JSONL format
            lines.append(json.dumps(data))
        except:
            continue
    return lines

def generate_coding_examples(topic, count=5):
    prompt = f"""
Generate {count} high-quality coding interaction examples for the topic: "{topic}".

Each example MUST be a JSON object with a "messages" list, following the OpenAI/Gemma chat format.
Example: {{"messages": [{{"role": "user", "content": "..."}}, {{"role": "assistant", "content": "..."}}]}}

Each example MUST be a single line JSON object in JSONL format.
Focus on complex, real-world scenarios and idiomatic code.
Include tool usage (JSON format) where appropriate.

Output ONLY the JSON lines, one per line.
"""
    try:
        result = subprocess.run(
            ["python3", "/tmp/gemma4.py", "-p", prompt],
            capture_output=True, text=True, check=True
        )
        return extract_json_lines(result.stdout)
    except Exception as e:
        print(f"Error generating for {topic}: {e}")
        return []

if __name__ == "__main__":
    topics_file = "topics.txt"
    if not os.path.exists(topics_file):
        print(f"Error: {topics_file} not found.", file=sys.stderr)
        sys.exit(1)
        
    with open(topics_file, "r") as f:
        topics = [line.strip() for line in f if line.strip()]
        
    output_file = "coding_data_200.jsonl"
    target_total = 200
    current_count = 0
    
    print(f"Starting generation of {target_total} examples...")
    
    with open(output_file, "w") as f:
        while current_count < target_total:
            for topic in topics:
                if current_count >= target_total:
                    break
                    
                print(f"  Generating for topic: {topic}")
                examples = generate_coding_examples(topic, count=5)
                
                if not examples:
                    print(f"    WARNING: No examples found in output for {topic}")
                    continue
                    
                for line in examples:
                    if current_count < target_total:
                        f.write(line + "\n")
                        current_count += 1
            
            print(f"  Total progress: {current_count}/{target_total}")
            
            # Small sleep to avoid hitting rate limits if any
            time.sleep(1)
            
    print(f"\nDone! Total generated: {current_count} examples saved to {output_file}")
