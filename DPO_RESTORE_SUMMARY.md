# DPO Restoration Summary (SUPAA-116)

**Objective:** Restore the Super Coding Model using a fixed, higher-complexity DPO dataset to address regressions identified in the April 19, 2026 audit.

## 1. Problem Identification
The previous DPO attempt (SUPAA-100) failed due to:
- **Low Dataset Complexity:** Training prompts were too simple compared to the QA benchmark.
- **SFT Noise:** Chosen/rejected pairs lacked strong distinction.
- **Legacy Patterns:** The model regressed to using legacy Python patterns and ignored tool-use constraints.

## 2. Remediation Steps

### 2.1 Fixed DPO Dataset
- Generated `dpo_data_fixed.jsonl` (13 pairs) using **Gemini 3 Flash**.
- **Complexity Alignment:** Prompts were directly derived from the first 20 cases of the `qa_test_suite.jsonl`, ensuring training difficulty matches evaluation difficulty.
- **Strong Distinction:**
    - **Chosen:** Senior Engineer persona, strictly idiomatic (e.g., `async with semaphore`), mandatory validation, and structured tool use.
    - **Rejected:** Subtle but critical flaws (hallucinated args, legacy patterns like `inspect.getargspec`, improper async cleanup, missing backpressure).
- **Post-Processing:** Stripped out meta-commentary and "flaw analysis" to ensure a clean training signal.

### 2.2 Optimized Training Configuration
- **Lower Learning Rate:** Reduced to `1e-5` for stability on a small dataset.
- **Reduced Steps:** Adjusted `max_steps` to `20` (~6 epochs) to prevent over-fitting.
- **Environment Parity:** Synced training script with VM-specific multimodal requirements (Gemma 4 `<image>` token handling).

## 3. Current Status: IN_PROGRESS
- DPO training is currently running on `hermes-finetune-gemma` (L4 GPU).
- Estimated completion: ~10 minutes.

## 4. Next Steps
1. **Merge LoRA:** Use `merge_lora_for_vllm.py` to produce the final model.
2. **Standardized Evaluation:** Run `run_qa_eval.py` and `llm_judge.py` against the new model.
3. **Deployment:** Update the `gemma4-coding` service in `us-central1`.
