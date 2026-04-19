import torch
from unsloth import FastLanguageModel, PatchDPOTrainer
PatchDPOTrainer()
from trl import DPOTrainer, DPOConfig
from datasets import load_dataset
import os

model_name = "gemma4-coding-adapter" # Start from SFT model

print("Loading model and tokenizer...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = model_name,
    max_seq_length = 2048,
    load_in_4bit = True,
)

if not hasattr(model, "peft_config"):
    print("Adding PEFT adapter...")
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
else:
    print("Model already has PEFT adapter. Using existing one for DPO.")

print("Loading dataset...")
if not os.path.exists("dpo_data.jsonl"):
    print("Error: dpo_data.jsonl not found!")
    exit(1)

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
dataset = dataset.map(prep_dpo_data, remove_columns=dataset.column_names, num_proc=1)

print("Setting up DPOTrainer...")
dpo_trainer = DPOTrainer(
    model = model,
    ref_model = None,
    args = DPOConfig(
        per_device_train_batch_size = 1,
        gradient_accumulation_steps = 8,
        warmup_steps = 5,
        max_steps = 40,
        learning_rate = 5e-5,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.0,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs_dpo_fixed",
        beta = 0.1,
        max_length = 1024,
        max_prompt_length = 512,
        dataset_num_proc = 1, # Use 1 to avoid hangs
    ),
    train_dataset = dataset,
    tokenizer = tokenizer,
)

print("Starting DPO training...")
dpo_trainer.train()

print("Saving DPO model...")
model.save_pretrained("gemma4-coding-dpo-adapter-fixed")
tokenizer.save_pretrained("gemma4-coding-dpo-adapter-fixed")
print("Done!")
