export interface EvalScore {
  correctness: number;
  instruction_following: number;
  idiomaticity: number;
  pedagogical_value: number;
  conciseness: number;
}

export interface Evaluation {
  topic: string;
  prompt: string;
  response: string;
  duration: number;
  tokens: number;
  tps: number;
  evaluation: {
    scores: EvalScore;
    justification: string;
  };
  weighted_score: number;
}

export interface BenchmarkData {
  summary: {
    total_cases: number;
    average_scores: EvalScore & { total_weighted: number };
  };
  evaluations: Evaluation[];
}

export const benchmarkData: BenchmarkData = {
  "summary": {
    "total_cases": 5,
    "average_scores": {
      "correctness": 0.6,
      "instruction_following": 4.2,
      "idiomaticity": 4.8,
      "pedagogical_value": 4.8,
      "conciseness": 5.0,
      "total_weighted": 3.8
    }
  },
  "evaluations": [
    {
      "topic": "Multi-Step Research & Fix",
      "prompt": "Identify all files in the repository that use 'deprecated_logger' and replace them with the new 'StandardLogger' class. After replacement, ensure that all modified files pass a basic syntax check. Do not commit changes.",
      "response": "This task requires a multi-step process: 1) finding all instances of the old logger, 2) replacing the import and usage, and 3) running a linter/syntax checker.\n\nHere is a conceptual plan using a combination of `grep` and `sed` for the replacement, followed by a conceptual call to a linter.\n\n### 1. Find all files using `deprecated_logger`\n\n```bash\ngrep -r \"import deprecated_logger\" .\n```\n\n### 2. Replace the usage (Conceptual `sed` command)\n\nWe need to replace the import and the instantiation/usage pattern.\n\n```bash\n# 1. Replace the import statement\nsed -i 's/import deprecated_logger/import StandardLogger/' $(grep -r \"import deprecated_logger\" .)\n\n# 2. Replace the instantiation/usage (This is highly dependent on how it's used, \n# but a general pattern might look like this)\nsed -i 's/deprecated_logger.get_logger()/StandardLogger.get_logger()/g' $(grep -r \"deprecated_logger\" .)\n```\n\n### 3. Verify Syntax\n\nAfter the replacements, run a linter (e.g., `pylint` or `flake8`) on the entire codebase to ensure no new syntax errors were introduced.\n\n```bash\npylint .\n```\n\n**Rationale:** Using `grep` first limits the scope of the `sed` command, making the replacement safer and faster. The final `pylint` step is crucial to fulfill the requirement of ensuring the modified files are syntactically correct.\n\n***\n\n**Note:** The `sed` commands above are illustrative. In a real-world scenario, a dedicated tool like `sed` or a specialized refactoring tool (like `ripgrep` combined with a custom script) is often safer for complex replacements than a single `sed` command, as context matters greatly for imports and usage patterns.",
      "duration": 3.753249406814575,
      "tokens": 418,
      "tps": 111.3701634751636,
      "evaluation": {
        "scores": {
          "correctness": 1,
          "instruction_following": 5,
          "idiomaticity": 5,
          "pedagogical_value": 5,
          "conciseness": 5
        },
        "justification": "The AI provided a conceptually correct and highly idiomatic solution for a command-line-based refactoring task. The breakdown into find, replace, and verify steps is logical and follows best practices. While the example `sed` commands would fail in a literal copy-paste due to `grep`'s default output format (it would require the `-l` flag), the response wisely qualifies the code as 'conceptual' and 'illustrative,' and the accompanying explanation and rationale are excellent. The pedagogical value is high, as it not only provides a solution but also explains the reasoning and potential pitfalls, which is what a senior engineer would do."
      },
      "weighted_score": 5.0
    },
    {
      "topic": "Dependency Management & Bug Fix",
      "prompt": "Check if 'requests' library is used in the project. If so, verify if it's pinned to a secure version (>2.31.0). If not, update the requirements.txt and fix any breaking changes in the code that uses 'requests'. Run existing tests to verify.",
      "response": "This task requires reading a `requirements.txt` file, parsing it, checking the version constraint for `requests`, modifying the file if necessary, and then running tests.\n\nHere is a complete Python script that performs this check and update, assuming a standard `requirements.txt` structure.\n\n### Python Script (`update_deps.py`)\n\n```python\nimport re\nimport subprocess\nimport sys\nfrom typing import List\n\ndef check_and_update_requests(requirements_file: str = \"requirements.txt\", min_version: str = \"2.31.0\"):\n    \"\"\"\n    Checks the requirements.txt for the 'requests' package. If the version is \n    less than the specified minimum, it updates the line and writes back to the file.\n    \"\"\"\n    print(f\"--- 1. Checking {requirements_file} for 'requests' ---\")\n    \n    try:\n        with open(requirements_file, 'r') as f:\n            lines = f.readlines()\n    except FileNotFoundError:\n        print(f\"Error: {requirements_file} not found.\")\n        return\n\n    new_lines = []\n    requests_found = False\n    updated = False\n    \n    # Regex to capture package name and version (e.g., 'requests==2.28.1' or 'requests>=2.20.0')\n    # This is a simplified regex; a more robust parser might be needed for complex dependency files.\n    pattern = re.compile(r\"^(requests[<=>!~]=?)(.*)$\")\n    \n    for line in lines:\n        match = pattern.match(line.strip())\n        \n        if match:\n            requests_found = True\n            operator = match.group(1)\n            current_version_spec = match.group(2).strip()\n            \n            # Simple check: if it's an exact pin (==) and the version is too old\n            if operator.startswith('==') and current_version_spec.split('==')[1] < min_version:\n                new_line = f\"requests=={min_version}\\n\"\n                new_lines.append(new_line)\n                print(f\"  [UPDATE] Found old version. Changing '{line.strip()}' to 'requests=={min_version}'\")\n                updated = True\n            else:\n                new_lines.append(line)\n        else:\n            new_lines.append(line)\n\n    if updated:\n        print(f\"\\n--- 2. Writing updated {requirements_file} ---\")\n        with open(requirements_file, 'w') as f:\n            f.writelines(new_lines)\n        print(\"Successfully updated 'requests' version in requirements.txt.\")\n    elif not requests_found:\n        print(\"Warning: 'requests' package not found in requirements.txt. Adding it now.\")\n        new_line = f\"requests=={min_version}\\n\"\n        with open(requirements_file, 'a') as f:\n            f.write(new_line)\n        print(\"Successfully added 'requests' to requirements.txt.\")\n    else:\n        print(\"Requests is already pinned to a version >= 2.31.0. No changes needed.\")\n\n    # --- 3. Install dependencies and run tests ---\n    print(\"\\n--- 3. Installing dependencies and running tests ---\")\n    try:\n        # Install/Upgrade dependencies\n        print(\"Running 'pip install -r requirements.txt'...\")\n        subprocess.run([sys.executable, \"-m\", \"pip\", \"install\", \"-r\", requirements_file], check=True)\n        \n        # Run tests (assuming 'pytest' is the test runner)\n        print(\"Running tests...\")\n        result = subprocess.run([\"pytest\"], capture_output=True, text=True)\n        \n        if result.returncode == 0:\n            print(\"\\n\\u2705 Success: Dependencies updated and all tests passed after upgrade.\")\n        else:\n            print(\"\\n\\u274c Failure: Tests failed after updating 'requests'. Review the output below.\")\n            print(\"--- Test Output Start ---\")\n            print(result.stdout)\n            print(\"--- Test Output End ---\")\n            sys.exit(1)\n\n    except subprocess.CalledProcessError as e:\n        print(f\"\\n\\u274c Error during dependency installation or testing: {e}\")\n        sys.exit(1)\n    except FileNotFoundError:\n        print(\"\\n\\u274c Error: 'pytest' command not found. Ensure pytest is installed.\")\n        sys.exit(1)\n\n\nif __name__ == \"__main__\":\n    pass",
      "duration": 8.802923202514648,
      "tokens": 1024,
      "tps": 116.3249952819631,
      "evaluation": {
        "scores": {
          "correctness": 0,
          "instruction_following": 4,
          "idiomaticity": 4,
          "pedagogical_value": 4,
          "conciseness": 5
        },
        "justification": "The response provides a well-structured script that correctly handles file I/O and running subprocesses to install dependencies and run tests. However, the core logic for version checking is fundamentally flawed, leading to a correctness score of 0. \n\nSpecifically, the script compares version numbers as strings ('2.9.0' > '2.10.0' would incorrectly evaluate to True), which is a classic bug. A proper version parsing library should be used. Secondly, it only attempts to update dependencies pinned with ==, ignoring other potentially insecure specifiers like >= or ~=."
      },
      "weighted_score": 2.0
    },
    {
      "topic": "Architectural Refactoring",
      "prompt": "The current project uses a flat directory structure. Propose and implement a 'src/' and 'tests/' separation for all Python files. Update necessary import paths and the test runner configuration to reflect this change.",
      "response": "This is a common and necessary refactoring step for any growing Python project. Separating source code from tests improves organization, clarity, and maintainability.\n\n### Proposed New Structure\n\n```\n.\n\\u251c\\u2500\\u2500 src/\n\\u2502   \\u251c\\u2500\\u2500 __init__.py\n\\u2502   \\u2514\\u2500\\u2500 utils.py\n\\u251c\\u2500\\u2500 tests/\n\\u2502   \\u251c\\u2500\\u2500 __init__.py\n\\u2502   \\u2514\\u2500\\u2500 test_utils.py\n\\u251c\\u2500\\u2500 main.py\n\\u2514\\u2500\\u2500 requirements.txt\n```",
      "duration": 7.957875728607178,
      "tokens": 930,
      "tps": 116.86535850978571,
      "evaluation": {
        "scores": {
          "correctness": 1,
          "instruction_following": 5,
          "idiomaticity": 5,
          "pedagogical_value": 5,
          "conciseness": 5
        },
        "justification": "The response is exemplary. It correctly identifies all necessary steps for the refactoring, including moving files, updating import paths in both application and test code, and configuring the test runner."
      },
      "weighted_score": 5.0
    }
  ]
};
