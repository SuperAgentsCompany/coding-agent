import torch
from unsloth import FastLanguageModel
from trl import DPOTrainer, DPOConfig
from datasets import load_dataset
import os

print("Loading model and tokenizer...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "gemma4-coding-adapter",
    max_seq_length = 2048,
    load_in_4bit = True,
)

# Ensure LoRA weights are trainable
print("Ensuring weights are trainable...")
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
    }

print("Preprocessing dataset...")
dataset = dataset.map(prep_dpo_data, remove_columns=dataset.column_names)

print("Setting up DPOTrainer...")
# Hack for Gemma 4 if needed by DPOTrainer
original_model_type = model.config.model_type
model.config.model_type = "llama" 

dpo_trainer = DPOTrainer(
    model = model,
    ref_model = None,
    args = DPOConfig(
        per_device_train_batch_size = 1,
        gradient_accumulation_steps = 8,
        warmup_steps = 5,
        max_steps = 40,
        learning_rate = 5e-5,
        bf16 = True,
        output_dir = "outputs_dpo_v6",
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
model.save_pretrained("gemma4-coding-dpo-adapter-v6")
tokenizer.save_pretrained("gemma4-coding-dpo-adapter-v6")
print("Done!")
