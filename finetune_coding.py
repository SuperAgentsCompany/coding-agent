from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset
import os

max_seq_length = 1024
dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.

print("Loading model and tokenizer...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "./gemma-4-E4B-it",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0, # Supports any, but = 0 is optimized
    bias = "none",    # Supports any, but = "none" is optimized
    use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
    random_state = 3407,
    use_rslora = False,  # We support rank stabilized LoRA
    loftq_config = None, # And LoftQ
)

def formatting_prompts_func(examples):
    instructions = examples["user"]
    outputs      = examples["assistant"]
    texts = []
    for instruction, output in zip(instructions, outputs):
        text = f"<start_of_turn>user\n{instruction}<end_of_turn>\n<start_of_turn>model\n{output}<end_of_turn>"
        texts.append(text)
    return { "text" : texts, }

print("Loading dataset...")
# Load the dataset
if not os.path.exists("coding_data.jsonl"):
    print("Error: coding_data.jsonl not found!")
    exit(1)

dataset = load_dataset("json", data_files="coding_data.jsonl", split="train")

# Preprocess the dataset to match the chat format
def prep_data(example):
    messages = example["messages"]
    user_msg = ""
    assistant_msg = ""
    for msg in messages:
        if msg["role"] == "user":
            user_msg = msg["content"]
        elif msg["role"] == "assistant":
            assistant_msg = msg["content"]
    return {"user": user_msg, "assistant": assistant_msg}

print("Preprocessing dataset...")
dataset = dataset.map(prep_data, remove_columns=["messages"])
dataset = dataset.map(formatting_prompts_func, batched = True,)

print("Setting up trainer...")
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False,
    args = TrainingArguments(
        per_device_train_batch_size = 1,
        gradient_accumulation_steps = 8,
        warmup_steps = 5,
        max_steps = 60,
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
    ),
)

print("Starting training...")
trainer_stats = trainer.train()

print("Saving model...")
model.save_pretrained("gemma4-coding-adapter")
tokenizer.save_pretrained("gemma4-coding-adapter")
print("Done!")
