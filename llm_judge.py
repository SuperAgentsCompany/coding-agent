import json
import os
import requests
import argparse
import time

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def judge_response(prompt, response, criteria):
    if not GEMINI_API_KEY:
        return {"error": "GEMINI_API_KEY not found"}

    system_prompt = f"""
You are an expert software engineer and QA Lead. Your task is to evaluate an AI's response to a coding prompt.
Evaluate based on the following criteria:
{json.dumps(criteria, indent=2)}

Provide a score from 1 to 5 for each criterion (except correctness which is 0 or 1), and a brief justification.

Return your evaluation as a JSON object with the following structure:
{{
  "scores": {{
    "correctness": 1,
    "instruction_following": 5,
    "idiomaticity": 5,
    "pedagogical_value": 5,
    "conciseness": 5
  }},
  "justification": "..."
}}
"""

    user_content = f"PROMPT:\n{prompt}\n\nRESPONSE:\n{response}"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": system_prompt + "\n\n" + user_content}]
        }],
        "generationConfig": {
            "response_mime_type": "application/json",
        }
    }
    
    try:
        # Rate limit prevention
        time.sleep(2)
        res = requests.post(url, json=payload, timeout=60)
        if res.status_code == 200:
            result = res.json()
            eval_text = result["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(eval_text)
        else:
            return {"error": f"API Error: {res.status_code} - {res.text}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", default="benchmark_results.jsonl", help="Benchmark results file")
    parser.add_argument("--config", default="benchmark_config.json", help="Config file")
    parser.add_argument("--output", default="evaluation_details.jsonl", help="Output details file (JSONL)")
    args = parser.parse_args()
    
    with open(args.config, "r") as f:
        config = json.load(f)
        
    criteria = config["metrics"]
    
    if not os.path.exists(args.results):
        print(f"Error: {args.results} not found.")
        sys.exit(1)
            
    print(f"Judging results from {args.results}...")
    
    # Load existing results to skip
    judged_topics = set()
    if os.path.exists(args.output):
        with open(args.output, "r") as f:
            for line in f:
                try:
                    res = json.loads(line)
                    judged_topics.add(res["topic"])
                except:
                    pass
    
    # Open output file in append mode
    with open(args.output, "a") as out_f:
        with open(args.results, "r") as f:
            for line in f:
                data = json.loads(line)
                topic = data['topic']
                
                if topic in judged_topics:
                    print(f"Skipping already judged topic: {topic}")
                    continue
                
                print(f"\nJudging Topic: {topic}...", end="", flush=True)
                evaluation = judge_response(data["prompt"], data["response"], criteria)
                
                if "error" in evaluation:
                    print(f" ERROR: {evaluation['error']}")
                    continue
                    
                print(" DONE")
                scores = evaluation.get("scores", {})
                
                c = scores.get("correctness", 0)
                if c == 0:
                    weighted_score = 2.0
                else:
                    weighted_score = (
                        c * criteria["correctness"]["weight"] * 5 + 
                        scores.get("instruction_following", 0) * criteria["instruction_following"]["weight"] +
                        scores.get("idiomaticity", 0) * criteria["idiomaticity"]["weight"] +
                        scores.get("pedagogical_value", 0) * criteria["pedagogical_value"]["weight"] +
                        scores.get("conciseness", 0) * criteria["conciseness"]["weight"]
                    )
                    
                data["evaluation"] = evaluation
                data["weighted_score"] = weighted_score
                
                out_f.write(json.dumps(data) + "\n")
                out_f.flush()
    
    print(f"\nEvaluation complete. Results saved to {args.output}")
