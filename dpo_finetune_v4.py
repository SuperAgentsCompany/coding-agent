import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, BitsAndBytesConfig
from peft import get_peft_model, LoraConfig, PeftModel
from trl import DPOTrainer, DPOConfig
from datasets import load_dataset
import os

model_id = "./gemma-4-E4B-it"
sft_adapter = "gemma4-coding-adapter"

print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_id)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    quantization_config=bnb_config,
)

print("Loading SFT adapter...")
model = PeftModel.from_pretrained(model, sft_adapter, is_trainable=True)

# Important: Make sure LoRA is trainable and fix target_modules if needed
# Actually PeftModel.from_pretrained with is_trainable=True should be enough.
# But let's be explicit.
for name, param in model.named_parameters():
    if "lora" in name:
        param.requires_grad = True

print("Loading dataset...")
dataset = load_dataset("json", data_files="dpo_data.jsonl", split="train")

def prep_dpo_data(example):
    prompt = f"<start_of_turn>user\n{example['prompt']}<end_of_turn>\n<start_of_turn>model\n"
    chosen = f"{example['chosen']}<end_of_turn>"
    rejected = f"{example['rejected']}<end_of_turn>"
    return {
        "prompt": prompt,
        "chosen": chosen,
        "rejected": rejected,
        "images": [], # Add empty images to avoid KeyError in multimodal-aware trainers
        "audios": [], # Add empty audios
    }

print("Preprocessing dataset...")
dataset = dataset.map(prep_dpo_data, remove_columns=dataset.column_names)

print("Setting up DPOTrainer...")
# Note: NOT using PatchDPOTrainer to avoid multimodal issues if any
original_model_type = model.config.model_type
model.config.model_type = "llama" # Necessary for some TRL versions with Gemma
model.warnings_issued = {}

dpo_trainer = DPOTrainer(
    model = model,
    ref_model = None,
    args = DPOConfig(
        per_device_train_batch_size = 1,
        gradient_accumulation_steps = 8,
        warmup_steps = 5,
        max_steps = 40,
        learning_rate = 5e-5,
        fp16 = False,
        bf16 = True,
        logging_steps = 1,
        optim = "adamw_torch",
        weight_decay = 0.0,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs_dpo_v4",
        beta = 0.1,
        max_length = 1024,
        max_prompt_length = 512,
        remove_unused_columns=False,
    ),
    train_dataset = dataset,
    processing_class = tokenizer,
)

model.config.model_type = original_model_type

print("Starting DPO training...")
dpo_trainer.train()

print("Saving DPO model...")
model.save_pretrained("gemma4-coding-dpo-adapter-v4")
tokenizer.save_pretrained("gemma4-coding-dpo-adapter-v4")
print("Done!")
