import os
import json
import subprocess
import sys

def get_topics(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def generate_prompt_for_topic(topic):
    prompt = f"""
I am building a high-quality QA test suite for a coding LLM. 
For the topic: "{topic}", please generate ONE extremely challenging and realistic coding prompt that a senior software engineer might ask.
The prompt should require a deep understanding of the topic, idiomatic patterns, and potential pitfalls.
It should be a "User Request" like: "I need to implement X using Y, but I have constraint Z. How do I do it?"

Output ONLY the prompt text. No markdown, no preamble.
"""
    try:
        # Use gemma4.py to generate the prompt
        result = subprocess.run(
            ["python3", "/tmp/gemma4.py", "-p", prompt],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error generating prompt for topic '{topic}': {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    topics = get_topics("topics.txt")
    qa_suite = []
    
    print(f"Generating QA suite for {len(topics)} topics...")
    for i, topic in enumerate(topics):
        print(f"[{i+1}/{len(topics)}] Topic: {topic}")
        prompt_text = generate_prompt_for_topic(topic)
        if prompt_text:
            # Clean up markdown if model included it
            prompt_text = prompt_text.replace("```", "").strip()
            if prompt_text.startswith("User Request:"):
                prompt_text = prompt_text.replace("User Request:", "").strip()
            
            qa_suite.append({
                "topic": topic,
                "prompt": prompt_text
            })
            print(f"  Generated prompt: {prompt_text[:100]}...")
    
    with open("qa_test_suite.jsonl", "w") as f:
        for item in qa_suite:
            f.write(json.dumps(item) + "\n")
    
    print(f"\nSaved {len(qa_suite)} test cases to qa_test_suite.jsonl")
