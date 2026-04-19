from unsloth import FastLanguageModel
import torch
from trl import DPOTrainer
from transformers import TrainingArguments

class PatchedTrainingArguments(TrainingArguments):
    def __getattr__(self, name):
        return None

from datasets import load_dataset
import os
from PIL import Image
import numpy as np

max_seq_length = 2048
dtype = None
load_in_4bit = True

print("Loading model and tokenizer...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "./gemma-4-E4B-it",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
)

print("Loading dataset...")
if not os.path.exists("dpo_data.jsonl"):
    print("Error: dpo_data.jsonl not found!")
    exit(1)

dataset = load_dataset("json", data_files="dpo_data.jsonl", split="train")

def prep_dpo_data(example):
    # Add <image> token to satisfy Gemma4Processor multimodal requirements
    prompt = f"<image><start_of_turn>user\n{example['prompt']}<end_of_turn>\n<start_of_turn>model\n"
    chosen = f"{example['chosen']}<end_of_turn>"
    rejected = f"{example['rejected']}<end_of_turn>"
    
    # Provide a valid dummy image
    img = Image.fromarray(np.zeros((224, 224, 3), dtype=np.uint8))
    
    return {
        "prompt": prompt,
        "chosen": chosen,
        "rejected": rejected,
        "images": [img],
    }

print("Preprocessing dataset...")
dataset = dataset.map(prep_dpo_data, remove_columns=dataset.column_names)

print("Setting up DPOTrainer...")
# Reduced max_steps and learning_rate for better stability with small high-quality dataset
dpo_trainer = DPOTrainer(
    model = model,
    ref_model = None,
    args = PatchedTrainingArguments(
        per_device_train_batch_size = 1,
        gradient_accumulation_steps = 4, # Reduced from 8 to have more frequent updates
        warmup_steps = 2,
        max_steps = 20, # 20 steps * 4 = 80 examples. 80 / 13 ~= 6 epochs.
        learning_rate = 1e-5, # Reduced from 5e-5 for stability
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.0,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs_dpo",
    ),
    beta = 0.1,
    train_dataset = dataset,
    tokenizer = tokenizer,
    max_length = max_seq_length,
    max_prompt_length = 512,
)

print("Starting DPO training...")
dpo_trainer.train()

print("Saving DPO model...")
model.save_pretrained("gemma4-coding-dpo-adapter")
tokenizer.save_pretrained("gemma4-coding-dpo-adapter")
print("Done!")
