# QA Audit Report: Super Coding Agent (Post-DPO)
**Date:** April 19, 2026
**Status:** 🔴 CRITICAL FAILURE / REGRESSION

## 1. Executive Summary
The post-DPO (Direct Preference Optimization) audit of the Super Coding Agent (Gemma4-Coding) reveals significant regressions and persistent reasoning failures across all evaluated agentic workflows. Despite claims in the Final Project Report, the model fails to adhere to critical instructions and produces syntactically correct but logically flawed (deadlocking) code in 84% of standardized tasks.

## 2. Key Audit Findings

### 2.1 Agentic Task Regressions (Compare to Baseline)
| Topic | Baseline Score | Post-DPO Score | Status |
| :--- | :---: | :---: | :--- |
| **Self-Correction & Testing** | 5.0 | 4.4 | 📉 Regression (Failed TDD flow) |
| **Multi-Step Research & Fix** | 5.0 | 5.0 | ✅ Stable |
| **Architectural Refactoring** | 5.0 | 2.0 | ❌ Critical Regression (Logic Error) |
| **Dependency Management** | 2.0 | 2.0 | ❌ Persistent Failure (Regex version check) |
| **Tool-Use Validation (.env)** | 2.0 | 2.0 | ❌ Persistent Failure (REDACTED vs Empty) |

### 2.2 Standardized Task Performance
- **Correctness Rate:** 16% (Down from expected >85%)
- **Average Weighted Score:** 2.44 / 5.0 (Target: 4.5)
- **Common Failure Pattern:** 
    - **`asyncio.TaskGroup` Deadlocks:** The model repeatedly places infinite loops (consumers) inside TaskGroups without a cancellation mechanism reachable by the group, causing the system to hang.
    - **Naive Automation:** Scripts generated for refactoring use arbitrary string matching (e.g., `item.startswith('src_')`) that does not correspond to the prompt or project structure.

## 3. Detailed Verification of SUPAA-84 Issues

### 3.1 .env File Handling (Failure)
- **Requirement:** Create `.env.example` with keys but *empty values*.
- **Actual Behavior:** The model continues to use `REDACTED` as the value in `.env.example`, ignoring the explicit instruction. This was the primary failure point DPO was intended to fix.

### 3.2 Implicit Constraints & Reasoning (Failure)
- **Requirement:** Verify if `requests` is pinned to a secure version (>2.31.0).
- **Actual Behavior:** The model uses a naive regex `re.search(r"requests==2\.\d{2}\.\d+", current_spec)` which fails to perform actual version comparison and ignores other specifiers like `>=`.

## 4. Pedagogical & Language Audit
- **Explanations:** The model maintains high pedagogical value (avg 4.8/5.0). It explains the code well, even when the code is broken.
- **Language:** Output is concise and professional, adhering to Paperclip standards.

## 5. Recommendations
1. **Immediate Rollback:** The DPO-merged model exhibits unacceptable regressions in architectural reasoning and TDD workflows.
2. **Data Audit:** Review the 15 DPO preference pairs. It appears the "Chosen" responses may not have been sufficiently distinctive or were outweighed by SFT noise.
3. **Re-training:** Re-initiate the DPO phase with a larger, more diverse set of preference pairs focusing specifically on `asyncio` structured concurrency and precise instruction following for tool-use.

---
**QA Lead Sign-off**
91b48bbf-7ca3-4431-b158-74b96eaced2a
