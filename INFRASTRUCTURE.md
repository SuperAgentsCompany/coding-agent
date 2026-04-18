# SUPAA Infrastructure

## Cloud Environment: Google Cloud Platform (GCP)
Project ID: `super-power-agents`

## Compute Resources
1.  **Serving (Cloud Run):**
    - Services: `gemma4-4b` (us-central1), `gemma4-coding` (us-central1, asia-southeast1)
    - Regions: `us-central1`, `asia-southeast1`
    - Hardware: 1x NVIDIA RTX Pro 6000 GPU.
    - Software: vLLM serving stack with OpenAI-compatible API.
2.  **Fine-tuning (Compute Engine):**
    - VM: `hermes-finetune-gemma`
    - Region: `asia-southeast1-b`
    - Hardware: 1x NVIDIA L4 GPU.
    - Software: PyTorch, Unsloth, HuggingFace Transformers.
3.  **Development VM:**
    - VM: `gemma-tuning-vm`
    - Region: `us-central1-a`
    - Hardware: 1x NVIDIA Tesla T4 GPU.

## Storage
- **Model Cache (GCS):** `gs://super-power-agents-model-cache/`
- **Dataset Storage:** Local `.jsonl` files in the Paperclip workspace, backed up to GCS.

## Networking
- **VPC:** `gemma-vpc`
- **Subnet:** `gemma-subnet`
- Cloud Run is publicly accessible via the authenticated endpoint, restricted to Paperclip agents and the Web MVP.
