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

## Super Coding Model Architecture
The Super Coding Model is a specialized version of Gemma4-4B, optimized for autonomous software engineering tasks. It employs a unique training and reasoning methodology to ensure high-fidelity tool usage and architectural integrity.

### 1. Code & QA Pair (CQP) Methodology
Our primary alignment strategy uses the CQP pattern, which pairs a technical objective with two distinct agentic responses:
- **Chosen (Senior Engineer + QA Lead):** This response follows a strict **Plan -> Act -> Validate** cycle. It prioritizes system-wide architectural integrity, mandatory post-execution validation (e.g., linting, testing), and concise, high-signal communication. It explicitly handles edge cases like structured concurrency (`asyncio.TaskGroup`) and security constraints.
- **Rejected (Legacy/Junior Patterns):** This response demonstrates anti-patterns such as:
    - Manual resource management (e.g., `acquire()`/`release()` instead of context managers).
    - Missing or hallucinated validation steps.
    - Conversational filler and verbose, low-signal explanations.
    - Hallucinated API arguments or legacy library usage (e.g., `inspect.getargspec`).

### 2. Training Pipeline (DPO)
The model is fine-tuned using **Direct Preference Optimization (DPO)** on top of a Supervised Fine-Tuning (SFT) base. This stage explicitly rewards the CQP "Chosen" trajectories, effectively training the model to think like a Senior Engineer who "trusts but verifies" their own code.

### 3. Agentic Orchestration
When integrated into the Paperclip layer, the Super Coding Model operates with a dedicated toolset for:
- **Research:** `grep_search`, `glob`, `read_file`.
- **Execution:** `run_shell_command`, `replace`, `write_file`.
- **Validation:** Automated execution of project-specific test runners and linters.

## Inference Data Flow
1. **Agent Task:** Paperclip orchestrates a task to the specialized agent.
2. **Inference:** Handled by the fine-tuned Gemma4 model served via vLLM.
3. **Reasoning Extraction:** The model's internal monologue is captured to provide transparency to the orchestrator.
4. **Tool Execution:** The model outputs bash, Python, or API tool-calls that are executed by the Paperclip adapter.
