# oryxa-ai

# Oryxa-AI Gemma Deployment Guide (RunPod GPU)

This guide documents the full process for deploying the `gemma-3-12b-it-q4_0.gguf` model on a RunPod A40 GPU instance using FastAPI and `llama-cpp-python` with CUDA support.

---

## Step 1: Clean the Project
- Removed `gemma-3-12b-it-q4_0.gguf` from `model/` to avoid 8GB GitHub limit
- Created empty `model/` folder with a `.gitkeep`
- Added `.gitignore`:
  ```
  *.gguf
  *.bin
  *.pt
  ```

---

## Step 2: Push Code to GitHub
- Uploaded project to a private repo: https://github.com/sallout/oryxa-ai

---

## Step 3: Deploy GPU Pod on RunPod
- Chose Secure Cloud with:
  - **1x A40 GPU**
  - **9 vCPU / 50 GB RAM**
  - **20 GB volume**
- Used `RunPod Pytorch 2.4.0` template
- Mounted volume at `/workspace`

---

## Step 4: Clone and Setup in Pod
```bash
cd /workspace
git clone https://<username>:<token>@github.com/sallout/oryxa-ai.git
cd oryxa-ai
```

---

## Step 5: Install System Dependencies
```bash
apt update && apt install -y \
  build-essential cmake git curl wget \
  python3 python3-pip libopenblas-dev
```

---

## Step 6: Install Python Requirements
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Step 7: Compile llama-cpp-python with CUDA
```bash
pip uninstall -y llama-cpp-python
CMAKE_ARGS="-DLLAMA_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir --force-reinstall
```

---

## Step 8: Download the Model
```bash
mkdir -p model
HF_TOKEN=hf_xxx
wget --header="Authorization: Bearer ${HF_TOKEN}" \
  https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-gguf/resolve/main/gemma-3-12b-it-q4_0.gguf \
  -O model/gemma-3-12b-it-q4_0.gguf
```

---

## Step 9: Run the FastAPI Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
You should see:
```
CUDA available: True
Model loaded successfully!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Step 10: Make API Request
Use Postman or curl:
```bash
POST http://<POD_IP>:8000/v1/chat/completions
{
  "messages": [
    { "role": "user", "content": "Hello!" }
  ]
}
```

---

## Restart Instructions (If Pod Is Reset)

After restarting the pod:

1. SSH or Web Terminal:
```bash
cd /workspace/oryxa-ai
```

2. Reinstall dependencies:
```bash
apt update && apt install -y \
  build-essential cmake git curl wget \
  python3 python3-pip libopenblas-dev
pip install --upgrade pip
pip install -r requirements.txt
pip uninstall -y llama-cpp-python
CMAKE_ARGS="-DLLAMA_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir --force-reinstall
```

3. Rerun server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

All project files and model will remain intact because they are stored in `/workspace` volume.

---

# in case of updating github In the RunPod terminal:
If Server Is Running ( Stop the services)
Press Ctrl + C to stop the FastAPI server

- Move to model folder and pull the cahnges 
cd /workspace/oryxa-ai
git pull

- Reinstall system & Python packages:
  ```bash
  apt update && apt install -y \
  build-essential cmake git curl wget \
  python3 python3-pip libopenblas-dev

  pip install --upgrade pip
  pip install -r requirements.txt

  # Rebuild llama-cpp-python with CUDA
  pip uninstall -y llama-cpp-python
  CMAKE_ARGS="-DLLAMA_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir --force-reinstall
``
Then restart it (session will be terminated once you close the web-terimnal):
uvicorn app.main:app --host 0.0.0.0 --port 8000

to start the service permanently use
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > log.txt 2>&1 &

# OR TO AVOID WRITING COMMAND, CREATE YOUR start.sh
  ```bash
#!/bin/bash

# Step 1: Go to workspace
cd /workspace

# Step 2: Clone or pull latest code
if [ ! -d "oryxa-ai" ]; then
  echo "Cloning repository..."
  git clone https://YOUR_GITHUB_USERNAME:YOUR_GITHUB_TOKEN@github.com/sallout/oryxa-ai.git
else
  echo "Pulling latest code from GitHub..."
  cd oryxa-ai
  git pull
fi

cd /workspace/oryxa-ai

# Step 3: Reinstall Python packages
echo "Installing Python packages..."
pip install -r requirements.txt
pip uninstall -y llama-cpp-python
CMAKE_ARGS="-DLLAMA_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir --force-reinstall

# Step 4: Run FastAPI server in background
echo "Starting server..."
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > log.txt 2>&1 &

echo "✅ Oryxa-AI server started. Logs -> log.txt"

```

#How to Set It Up in RunPod
Save the file:

nano /workspace/start.sh

Paste the content, then save (Ctrl + O, Enter, then Ctrl + X)

#Make it executable:
chmod +x /workspace/start.sh

#Run it anytime:
/workspace/start.sh


> Maintained by: @sallout | Project: Oryxa AI | Last updated: 2025-06-05
