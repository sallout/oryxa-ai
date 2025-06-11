import json
from llama_cpp import Llama
import torch

print(f"CUDA available: {torch.cuda.is_available()}")  # Check GPU

# Load the model with explicit error handling
try:
    llm = Llama(
        model_path="./model/gemma-3-12b-it-q8_0.gguf",
        n_ctx=2048,
        n_threads=8,
        n_gpu_layers= -1,  # <---- force full GPU offloading
        verbose=False  # Enable verbose logging
    )
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Model loading failed: {e}")
    raise

# Load the prompt template and metadata once
with open("prompt.txt", "r") as f:
    base_prompt_template = f.read()

with open("metadata.json", "r") as f:
    metadata = json.load(f)

# Insert metadata into the system prompt
metadata_json_str = json.dumps(metadata, indent=2)
base_prompt = base_prompt_template.replace("metadata_placeholder", metadata_json_str)

# Exposed function to generate a response(works with gemma)
def generate_completion(conversation: list) -> str:
    messages = [{"role": "system", "content": base_prompt}] + conversation

    output = llm.create_chat_completion(
        messages=messages,
        temperature=0.2,
        max_tokens=4096
    )
    return output["choices"][0]["message"]["content"]


