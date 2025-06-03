from llama_cpp import Llama

llm = Llama(
    model_path="./model/gemma-3-12b-it.Q4_K_M.gguf",
    n_ctx=4096,
    n_threads=8
)

with open("prompt.txt", "r") as f:
    base_prompt = f.read()

def generate_completion(user_message):
    full_prompt = f"{base_prompt}\nUser: {user_message}\nAssistant:"
    output = llm(full_prompt, max_tokens=512, stop=["User:", "Assistant:"])
    return output["choices"][0]["text"].strip()