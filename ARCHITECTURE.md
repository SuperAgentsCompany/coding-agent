# Coding Agent System Architecture

## Overview
The **Super Coding Model** is an agentic platform designed for high-precision autonomous software engineering, integrated into the SUPAA orchestration layer.

## Core Components
1. **Gemma4-4b Base Model:** Our foundational LLM, chosen for its high performance at a small scale (4B parameters), native tool-use, and reasoning capabilities.
2. **Super Coding Adapter (LoRA/DPO):** Low-Rank Adaptation (LoRA) and Direct Preference Optimization (DPO) applied to specialize the base model for complex software engineering workflows.
3. **Orchestration Layer (Paperclip):** Manages agent workflows, tool execution, and delegation using the fine-tuned model via a vLLM endpoint.

## Data Generation Pipeline
High-quality synthetic pedagogical data and coding interactions are generated to bootstrap performance:
- `generate_coding_data.py`: Generates the initial Supervised Fine-Tuning (SFT) dataset.
- `generate_dpo_pairs.py`: Produces preference pairs (chosen vs. rejected) for DPO alignment.

## Model Specialization Pipeline
1. **Supervised Fine-Tuning (SFT):** `finetune_coding.py` trains the base model using Unsloth (or raw Hugging Face `trl`/`peft`) on GCP L4 GPUs.
2. **Direct Preference Optimization (DPO):** `dpo_finetune_coding.py` aligns the model with our desired coding behaviors using TRL's `DPOTrainer`.
3. **Evaluation:** `run_benchmark.py` and `evaluate_coding.py` benchmark the model against the base model for domain-specific accuracy (Pass@1, etc.). `llm_judge.py` is used for qualitative scoring.
4. **Deployment:** The combined LoRA weights are merged and served via vLLM on GCP Cloud Run.

## Inference Data Flow
1. **Agent Task:** Paperclip orchestrates a task to the specialized agent.
2. **Inference:** Handled by the fine-tuned Gemma4 model served via vLLM.
3. **Reasoning Extraction:** The model's internal monologue is captured to provide transparency to the orchestrator.
4. **Tool Execution:** The model outputs bash, Python, or API tool-calls that are executed by the Paperclip adapter.
