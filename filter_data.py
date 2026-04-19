import json
import sys

def filter_jsonl(input_file, output_file):
    valid_count = 0
    invalid_count = 0
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                # Check structure
                if "messages" in data and isinstance(data["messages"], list):
                    has_user = any(m.get("role") == "user" for m in data["messages"])
                    has_assistant = any(m.get("role") == "assistant" for m in data["messages"])
                    if has_user and has_assistant:
                        f_out.write(json.dumps(data) + "\n")
                        valid_count += 1
                    else:
                        invalid_count += 1
                else:
                    invalid_count += 1
            except Exception as e:
                print(f"Error parsing line: {e}")
                invalid_count += 1
    
    print(f"Filtered {input_file}: {valid_count} valid, {invalid_count} invalid.")

if __name__ == "__main__":
    filter_jsonl("coding_data.jsonl", "coding_data_fixed.jsonl")
