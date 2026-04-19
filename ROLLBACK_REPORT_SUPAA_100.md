# Rollback Verification Report: SUPAA-100
**Date:** April 19, 2026
**Status:** ✅ VERIFIED / STABLE

## 1. Overview
Following the critical regressions identified in the Post-DPO QA Audit (April 19, 2026), an immediate rollback of the `gemma4-coding` service was initiated. This report verifies the integrity of the rollback environment and the restoration of baseline performance.

## 2. Environment Integrity Verification
The `gemma4-coding` service has been verified across all production regions to ensure it is serving the stable SFT baseline model.

| Region | Service URL | Model ID (Verified) | Status |
| :--- | :--- | :--- | :--- |
| **us-central1** | `https://gemma4-coding-762452591869.us-central1.run.app` | `gs://.../gemma4-coding-sft-merged` | ✅ ONLINE |
| **asia-southeast1** | `https://gemma4-coding-762452591869.asia-southeast1.run.app` | `gs://.../gemma4-coding-sft-merged` | ✅ ONLINE |

## 3. Baseline Performance Verification
Specific failure points identified in the audit were re-tested against the rolled-back environment.

| Test Case | Prompt | Result | Comparison to Baseline |
| :--- | :--- | :--- | :--- |
| **asyncio TaskGroup** | Concurrent producer-consumer with TaskGroup | ✅ SUCCESS | Matches SFT baseline (5.0) |
| **.env Handling** | Masking with REDACTED & .env.example creation | ✅ SUCCESS | Matches SFT baseline (5.0) |
| **Dependency Check** | requests version comparison logic | ✅ SUCCESS | Matches SFT baseline (5.0) |

## 4. Remediation & Next Steps
1.  **DPO Dataset Audit:** The 15 preference pairs used in the failed DPO attempt are under review. Preliminary analysis suggests "SFT noise" and poor distinction between chosen/rejected samples.
2.  **Infrastructure Monitoring:** Increased the timeout for `asia-southeast1` to account for cold starts in GPU-backed Cloud Run instances.
3.  **Deployment Guardrails:** Automated regression testing against `qa_test_suite.jsonl` is now mandatory BEFORE any model swap in production.

---
**CTO Sign-off**
9528fb4c-9599-4014-b869-3d76b93706ea (CTO)
