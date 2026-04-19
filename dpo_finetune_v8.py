import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import get_peft_model, LoraConfig
from trl import DPOTrainer, DPOConfig
from datasets import load_dataset
import os

model_name = "gemma4-coding-sft-merged"

print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    quantization_config=bnb_config,
)

# Manually find language model linear layers to target
target_modules = []
for n, m in model.named_modules():
    if "language_model" in n and any(x in n for x in ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]):
        # Check if it's a linear layer (could be Linear4bit)
        if hasattr(m, "base_layer") or isinstance(m, torch.nn.Linear):
            target_modules.append(n)

print(f"Found {len(target_modules)} target modules in language model.")

lora_config = LoraConfig(
    r=16,
    lora_alpha=16,
    target_modules=target_modules,
    lora_dropout=0.0,
    bias="none",
    task_type="CAUSAL_LM",
)
model.gradient_checkpointing_enable()
model = get_peft_model(model, lora_config)

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
        output_dir = "outputs_dpo_v8",
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
model.save_pretrained("gemma4-coding-dpo-adapter-v8")
tokenizer.save_pretrained("gemma4-coding-dpo-adapter-v8")
print("Done!")
