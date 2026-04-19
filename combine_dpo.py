import os
import json
import re

def clean_response(text):
    # Remove "Subtle Flaw Analysis" sections or similar
    text = re.split(r'\n#{1,3}\s*Subtle Flaw Analysis', text, flags=re.IGNORECASE)[0]
    text = re.split(r'\n\*\*Subtle Flaw Analysis\*\*', text, flags=re.IGNORECASE)[0]
    return text.strip()

output_file = "dpo_data_combined.jsonl"
count = 0
with open(output_file, "w") as out_f:
    for part in ["aa", "ab", "ac", "ad"]:
        filename = f"dpo_part_{part}.jsonl"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        data["chosen"] = clean_response(data["chosen"])
                        data["rejected"] = clean_response(data["rejected"])
                        out_f.write(json.dumps(data) + "\n")
                        count += 1
                    except:
                        pass

print(f"Combined {count} pairs into {output_file}")
