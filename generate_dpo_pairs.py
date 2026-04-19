import subprocess
import json
import os
import re

def generate_dpo_pair(topic, prompt_text):
    # Prompt for the "Good" (Chosen) response
    good_prompt = f"""
Topic: {topic}
Task: {prompt_text}

Provide a high-quality, professional, and concise response as a senior software engineer.
If the task requires multiple steps, provide a clear plan.
If tool use is implied, show how you would use them (e.g., using JSON tool call format).
Crucially, include validation steps (e.g., running tests, checking syntax).
Follow Paperclip standards: high signal, low noise.

Output ONLY the response content.
"""

    # Prompt for the "Bad" (Rejected) response
    bad_prompt = f"""
Topic: {topic}
Task: {prompt_text}

Provide a response that has one or more of the following flaws:
1. Hallucinated tool names or arguments.
2. Missing validation steps after making changes.
3. Overly verbose with low-signal chitchat.
4. Slightly incorrect code or logic.
5. Ignoring a constraint mentioned in the prompt.

Output ONLY the response content.
"""

    def get_res(p):
        try:
            result = subprocess.run(
                ["python3", "/tmp/gemma4.py", "-p", p],
                capture_output=True, text=True, check=True
            )
            # Remove the session ID and system messages from the output if any
            lines = result.stdout.splitlines()
            content = []
            for line in lines:
                if not line.startswith('{"type":'):
                    content.append(line)
            return "\n".join(content).strip()
        except Exception as e:
            print(f"Error: {e}")
            return None

    print(f"Generating GOOD response for: {topic}")
    chosen = get_res(good_prompt)
    print(f"Generating BAD response for: {topic}")
    rejected = get_res(bad_prompt)
    
    if chosen and rejected:
        return {
            "prompt": prompt_text,
            "chosen": chosen,
            "rejected": rejected
        }
    return None

if __name__ == "__main__":
    test_cases = [
        {"topic": "asyncio: Structured Concurrency", "prompt": "Implement a concurrent worker pool using asyncio.TaskGroup. Ensure workers can be shut down gracefully using a sentinel value."},
        {"topic": "Security: SQL Injection Mitigation", "prompt": "Audit the following Python function for SQL injection vulnerabilities. If found, refactor it to use parameterized queries and add a unit test that attempts an injection."},
        {"topic": "Performance: Optimizing JSON Processing", "prompt": "The current script processes a 1GB JSON file slowly. Propose an optimization using streaming (e.g., ijson or similar) and implement a benchmark to compare the two approaches."},
        {"topic": "Error Handling: Robust API Client", "prompt": "Enhance this simple API client with retry logic (exponential backoff), circuit breaker pattern, and detailed error logging for different HTTP status codes."},
        {"topic": "Refactoring: Replace Global State", "prompt": "Identify all uses of the global 'CONFIG' object in the 'services/' directory and refactor them to use dependency injection. Update the service factory to provide the configuration."},
        {"topic": "Tool Use: Log Analysis", "prompt": "Find the last 100 lines of 'access.log' containing '404' errors. Extract the unique URLs and identify the most frequent referring IP addresses using shell tools."},
        {"topic": "Testing: Mocking External Services", "prompt": "Write an integration test for 'PaymentService' that mocks the Stripe API response. Ensure the test covers both successful payment and card decline scenarios."},
        {"topic": "DevOps: Dockerfile Optimization", "prompt": "Review this Dockerfile. Implement multi-stage builds to reduce the image size and ensure that the application runs as a non-root user for security."},
        {"topic": "Documentation: Automated API Docs", "prompt": "Scan the 'api/' directory for Docstrings and generate a 'README_API.md' file that summarizes all endpoints, parameters, and return types."},
        {"topic": "Code Quality: Fixing Circular Imports", "prompt": "The project is failing to start due to a circular import between 'models.py' and 'schemas.py'. Analyze the dependencies and refactor the code to break the cycle."},
        {"topic": "Tool Use: Complex Search & Replace", "prompt": "Find all occurrences of 'utils.format_date(d, \"US\")' and replace them with 'dates.iso_format(d)'. Be careful with imports: add 'import dates' if missing and remove 'import utils' if it becomes unused."}
    ]
            
    output_file = "dpo_data.jsonl"
    for case in test_cases:
        pair = generate_dpo_pair(case["topic"], case["prompt"])
        if pair:
            with open(output_file, "a") as f:
                f.write(json.dumps(pair) + "\n")
            print(f"  Saved DPO pair for {case['topic']}")
