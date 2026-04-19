from unsloth import FastLanguageModel
import torch
import os

adapter_path = "gemma4-coding-dpo-adapter"
output_dir = "gemma4-coding-dpo-merged"

print("Loading model and adapter...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=adapter_path,
    max_seq_length=2048,
    dtype=torch.bfloat16,
    load_in_4bit=False,
)

print("Merging LoRA weights and saving...")
model.save_pretrained_merged(output_dir, tokenizer, save_method="merged_16bit")

print(f"Merged model saved to {output_dir}")
