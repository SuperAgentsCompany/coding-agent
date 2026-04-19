import json
import os
from collections import Counter

def analyze_suite(file_path):
    if not os.path.exists(file_path):
        return None
    
    topics = []
    languages = Counter()
    
    with open(file_path, "r") as f:
        for line in f:
            case = json.loads(line)
            topic = case["topic"]
            topics.append(topic)
            
            # Simple language detection from topic
            if "Python" in topic: languages["Python"] += 1
            elif "TypeScript" in topic or "TS" in topic or "React" in topic: languages["TypeScript"] += 1
            elif "Bash" in topic or "Shell" in topic: languages["Bash"] += 1
            elif "SQL" in topic: languages["SQL"] += 1
            elif "Node.js" in topic: languages["Node.js"] += 1
            elif "Security" in topic: languages["Security"] += 1
            elif "DevOps" in topic: languages["DevOps"] += 1
            elif "Architecture" in topic: languages["Architecture"] += 1
            else: languages["Other"] += 1
            
    return {
        "count": len(topics),
        "languages": dict(languages),
        "topics": topics
    }

if __name__ == "__main__":
    qa_report = analyze_suite("qa_test_suite.jsonl")
    agentic_report = analyze_suite("agentic_test_suite.jsonl")
    
    print("=== TEST SUITE COVERAGE REPORT ===")
    if qa_report:
        print(f"\nQA Standardized Tasks: {qa_report['count']}")
        for lang, count in qa_report['languages'].items():
            print(f"  - {lang}: {count}")
            
    if agentic_report:
        print(f"\nAgentic Multi-Step Tasks: {agentic_report['count']}")
        
    print("\nBenchmark Suite Preparation: COMPLETE")
