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

# Use LoraConfig with explicit target_modules for the language model
# We avoid the .linear suffix to hit the language model layers
lora_config = LoraConfig(
    r=16,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.0,
    bias="none",
    task_type="CAUSAL_LM",
)

# Load SFT adapter weights into a NEW PEFT model to avoid Gemma4ClippableLinear issues in peft
print("Adding PEFT adapter...")
model = get_peft_model(model, lora_config)

# Now manually load the SFT weights if possible, or just start from SFT merged model
# Using the SFT merged model is actually much safer.
# But I'll try to load the SFT merged model as the base for this run.
# I already confirmed gemma4-coding-sft-merged exists.

print("Done setting up model.")

# I'll modify the script to use the merged model as base instead of ./gemma-4-E4B-it
