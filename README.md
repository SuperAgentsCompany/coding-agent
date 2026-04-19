# SUPAA - Coding Agent

This repository contains the training scripts, data generation pipelines, and evaluation frameworks for the SUPAA **Super Coding Model**.

## Repository Structure

- `api/`, `src/`, `tests/`, `dashboard/`: Auxiliary source code and dashboards.
- `coding_data.jsonl`, `dpo_data.jsonl`, `qa_test_suite.jsonl`: Training and evaluation datasets.
- `finetune_coding.py`: Supervised Fine-Tuning (SFT) script for Gemma4.
- `dpo_finetune_coding.py`: Direct Preference Optimization (DPO) script.
- `generate_coding_data.py`, `generate_dpo_pairs.py`: Data generation pipelines.
- `evaluate_coding.py`, `run_benchmark.py`, `llm_judge.py`: Automated evaluation and benchmarking tools.

## Engineering Documentation Standard
All engineers contributing to this repository must follow the [SUPAA Engineering Documentation Standard](https://github.com/SuperAgentsCompany/documentations/blob/main/Engineering_Documentation_Standard.md).

## Getting Started

### Data Generation

To generate new coding examples or DPO pairs:
```bash
python generate_coding_data.py
python generate_dpo_pairs.py
```

### Training

To run the SFT or DPO training processes (requires GPU, recommended on GCP L4 or higher):
```bash
python finetune_coding.py
python dpo_finetune_coding.py
```

### Evaluation

To evaluate the fine-tuned model against the benchmark suite:
```bash
python run_benchmark.py
python llm_judge.py --results benchmark_results.jsonl --output evaluation.json
```

## Tech Stack
- **Model:** Gemma4-4b
- **Training:** PyTorch, Hugging Face Transformers, PEFT (LoRA), TRL (DPOTrainer).
- **Compute:** GCP Compute Engine (L4/RTX 6000 GPUs).
