from unsloth import FastLanguageModel
import torch
import os

adapter_path = "gemma4-coding-adapter"
output_dir = "gemma4-coding-merged"

print("Loading model and adapter...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=adapter_path,
    max_seq_length=1024,
    dtype=torch.bfloat16,
    load_in_4bit=False,
)

print("Merging LoRA weights and saving...")
# save_pretrained_merged saves the merged model in HF format (safetensors by default)
model.save_pretrained_merged(output_dir, tokenizer, save_method="merged_16bit")

print(f"Merged model saved to {output_dir}")
