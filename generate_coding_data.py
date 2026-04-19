import subprocess
import json
import os
import sys
import re

def generate_coding_examples(topic, count=5):
    prompt = f"""
Generate {count} new high-quality examples of coding interactions focusing on the topic: "{topic}".
Each example should be a JSON object on a single line (JSONL format).
The format MUST be:
{{"messages": [{{"role": "user", "content": "USER_REQUEST"}}, {{"role": "assistant", "content": "AGENT_RESPONSE"}}]}}

The USER_REQUEST should be a realistic coding problem, refactoring task, or tool-related request (e.g., "Search for X in the codebase", "Read file Y and fix the bug", "Implement feature Z").
The AGENT_RESPONSE should:
1. Be professional, direct, and concise.
2. Provide high-quality, idiomatic code snippets (Python, TypeScript, or Bash).
3. If appropriate, demonstrate tool usage or planning (e.g., "I will first search for...", "Plan: 1. Read file, 2. Apply fix, 3. Validate").
4. Explain the technical rationale behind the solution.

Output ONLY the JSONL lines. Do NOT include markdown code blocks. Do NOT include any preamble or postamble.
"""
    
    try:
        # Using the gemma4.py script in /tmp
        result = subprocess.run(
            ["python3", "/tmp/gemma4.py", "-p", prompt],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def extract_json_lines(text):
    lines = []
    potential_lines = text.splitlines()
    for line in potential_lines:
        line = line.strip()
        if not line: continue
        
        # Remove markdown backticks if present
        line = re.sub(r'^```jsonl?\s*', '', line)
        line = re.sub(r'```$', '', line)
        line = line.strip()
        
        if line.startswith("{") and line.endswith("}"):
            try:
                json.loads(line)
                lines.append(line)
            except:
                pass
    return lines

if __name__ == "__main__":
    topics = [
        "Python: asynchronous programming and asyncio",
        "Python: decorators and context managers",
        "TypeScript: generic types and utility types",
        "TypeScript: React hooks and state management",
        "Bash: file processing and text manipulation with awk/sed",
        "Tool Calling: searching codebase with grep/ripgrep",
        "Tool Calling: reading and editing files surgically",
        "Software Architecture: designing a scalable REST API",
        "Debugging: identifying and fixing memory leaks",
        "Testing: writing unit tests and integration tests with pytest/jest"
    ]
    
    output_file = "coding_data.jsonl"
    total_generated = 0
    
    for topic in topics:
        print(f"Generating for topic: {topic}...")
        output = generate_coding_examples(topic, count=10)
        if output:
            valid_lines = extract_json_lines(output)
            with open(output_file, "a") as f:
                for line in valid_lines:
                    f.write(line + "\n")
            total_generated += len(valid_lines)
            print(f"  Generated {len(valid_lines)} valid lines.")
    
    print(f"\nDone! Total generated: {total_generated} examples saved to {output_file}")
