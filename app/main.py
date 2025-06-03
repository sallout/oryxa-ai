from fastapi import FastAPI
from pydantic import BaseModel
from chat import generate_completion
import json

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/metadata")
def get_metadata():
    with open("metadata.json", "r") as f:
        return json.load(f)

@app.post("/v1/chat/completions")
def chat_completion(request: ChatRequest):
    reply = generate_completion(request.message)
    return {
        "id": "chatcmpl-001",
        "object": "chat.completion",
        "choices": [{"message": {"role": "assistant", "content": reply}}],
    }
