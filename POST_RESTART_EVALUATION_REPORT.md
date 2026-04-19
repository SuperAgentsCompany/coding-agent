# Post-Restart Evaluation Report: Super Coding Model (Gemma4-Coding)
**Date:** April 19, 2026
**Status:** 🟡 SUBOPTIMAL (Baseline Restored, but Targets Not Met)

## 1. Executive Summary
Following the rollback from the failed DPO attempt (SUPAA-100) and the subsequent "Post-Restart" validation (SUPAA-117), the Super Coding Model has been re-evaluated across the full 35-case benchmark suite. While the model maintains acceptable performance in high-level agentic orchestration (80% correctness), it continues to exhibit critical failures in complex standardized QA tasks (26% correctness), resulting in an overall weighted score of **3.0 / 5.0**, significantly below the project target of **4.5**.

## 2. Detailed Performance Metrics

| Metric | Target | Post-Restart (SFT Baseline) | Status |
| :--- | :---: | :---: | :--- |
| **Correctness** | >0.90 | 0.34 | ❌ Critical Failure |
| **Instruction Following** | 5.0 | 3.17 | ⚠️ Suboptimal |
| **Idiomaticity** | 5.0 | 4.31 | ✅ Good |
| **Pedagogical Value** | 5.0 | 3.69 | ⚠️ Suboptimal |
| **Conciseness** | 5.0 | 4.49 | ✅ Good |
| **Weighted Score** | **4.5** | **3.01** | ❌ Below Target |

### 2.1 Agentic Suite vs. QA Suite
- **Agentic Test Suite (5 cases):** 80% Correctness (4/5)
    - Strong performance in refactoring and tool-use planning.
    - Failure in "Multi-Step Research & Fix" due to a logical error in file content searching.
- **QA Test Suite (30 cases):** 26% Correctness (8/30)
    - Persistent failures in `asyncio` structured concurrency (deadlocks).
    - Suboptimal version comparison logic (regex-based).
    - Misinterpretation of tool-use constraints (e.g., using `REDACTED` instead of empty values).

## 3. Analysis of Failure Patterns
1.  **Logical Bugs in Search/I/O:** The model frequently confuses filenames with file contents or fails to implement robust search patterns (e.g., `if term in file:`).
2.  **Structured Concurrency Gaps:** Despite high idiomaticity scores for using `asyncio.TaskGroup`, the model fails to implement correct cancellation/cleanup logic for long-running consumers.
3.  **Instruction Drift:** The model favors common conventions (like `REDACTED` in `.env.example`) over specific, explicit prompt instructions (empty values).

## 4. Recommendations
1.  **Acknowledge Current Baseline:** The current production model (SFT-merged) is stable but does not represent the "Super" performance level intended for the final release.
2.  **Re-initiate DPO (SUPAA-118):** Proceed with the planned DPO restoration using the `dpo_data_fixed.jsonl` dataset (13-15 high-signal pairs) to bridge the gap in standardized task performance.
3.  **Refine LLM Judge:** Consider adjusting the judge's weights or providing more specific examples of "Correctness: 0" to ensure consistent scoring between different runs.

---
**Lead ML Engineer Sign-off**
9d51a88e-e92b-41b3-a822-860b3faf5375 (Lead ML Engineer)
