# Evaluation Criteria for Super Coding Model

This document defines the metrics used to evaluate the output of the Super Coding Model (Gemma4-Coding).

## 1. Primary Metrics (Quantitative)

### 1.1 Pass@1 (Correctness)
*   **Definition:** Can the generated code execute and produce the expected output?
*   **Measurement:**
    *   For Python: Run through a test runner (e.g., `pytest`).
    *   For SQL: Execute against a mock PostgreSQL database.
    *   For Bash: Execute in a sandboxed environment.
    *   For TypeScript/React: Static analysis (lint/type-check) + runtime simulation.
*   **Score:** Binary (0 or 1) per test case.

### 1.2 Instruction Following (Adherence)
*   **Definition:** Did the model follow all explicit constraints? (e.g., "no external libraries", "use asyncio.TaskGroup", "return as JSON").
*   **Measurement:** LLM-as-a-judge (Gemini-1.5-Pro) or manual audit.
*   **Score:** 1-5 (1: Ignored most, 5: Followed all).

### 1.3 Performance (Latency & Throughput)
*   **Measurement:**
    *   **Time to First Token (TTFT):** In milliseconds.
    *   **Tokens Per Second (TPS):** Total tokens / Generation time.
*   **Target:** > 50 TPS on production hardware.

## 2. Qualitative Metrics (Pedagogical & Style)

### 2.1 Idiomatic Quality
*   **Definition:** Does the code use modern, standard practices for the language? (e.g., Python 3.11+ features, TS 5.0+ features, ShellCheck compliance).
*   **Score:** 1-5.

### 2.2 Pedagogical Value
*   **Definition:** Are the explanations clear, concise, and helpful for a learner? Does it avoid "hallucinated" jargon?
*   **Score:** 1-5.

### 2.3 Conciseness (Paperclip Standard)
*   **Definition:** Does the model provide a high signal-to-noise ratio? Is it direct and professional?
*   **Score:** 1-5.

## 3. Scoring Formula

Total Score = (Correctness * 0.4) + (InstructionFollowing * 0.2) + (IdiomaticQuality * 0.15) + (PedagogicalValue * 0.15) + (Conciseness * 0.10)

*Note: If Correctness is 0, the total score is capped at 2.0/5.0 regardless of other metrics.*
