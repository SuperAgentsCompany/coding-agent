from unsloth import FastLanguageModel
import torch

max_seq_length = 1024
dtype = None
load_in_4bit = True

print("Loading model...", flush=True)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "gemma4-coding-adapter",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)
FastLanguageModel.for_inference(model)

print("Generating...", flush=True)
prompt = "<start_of_turn>user\nHello, who are you?<end_of_turn>\n<start_of_turn>model\n"
inputs = tokenizer(text=[prompt], return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=20)
print(tokenizer.batch_decode(outputs), flush=True)
