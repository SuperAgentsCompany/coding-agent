# SUPAA Infrastructure - Coding Agent

## Cloud Environment: Google Cloud Platform (GCP)
Project ID: `super-power-agents`

## Compute Resources
1.  **Serving (Cloud Run):**
    - Services: `gemma4-coding`
    - Region: `us-central1`
    - Hardware: 1x NVIDIA RTX Pro 6000 GPU (1 GPU per instance).
    - Memory: 80Gi
    - CPU: 20
    - Software: vLLM serving stack with OpenAI-compatible API.
    - Configuration: Deployed via `pytorch-vllm-serve:gemma4` container.
2.  **Fine-tuning (Compute Engine):**
    - VM: `hermes-finetune-gemma`
    - Region: `asia-southeast1-b`
    - Hardware: 1x NVIDIA L4 GPU.
    - Software: PyTorch, Unsloth, HuggingFace Transformers, PEFT, TRL.

## Storage
- **Model Cache (GCS):** `gs://super-power-agents-model-cache/models/`
- **Dataset Storage:** Local `.jsonl` files (e.g., `coding_data.jsonl`, `dpo_data.jsonl`) in the Paperclip workspace, backed up to GCS.

## Networking
- **VPC:** `gemma-vpc`
- **Subnet:** `gemma-subnet`
- **Service Account:** `762452591869-compute@developer.gserviceaccount.com`
- Cloud Run is publicly accessible via the authenticated endpoint, restricted to Paperclip agents and the Web MVP.
