FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system packages
RUN apt-get update && apt-get install -y \
    python3 python3-pip git curl wget \
    build-essential cmake libopenblas-dev \
    && apt-get clean

RUN pip3 install --upgrade pip

WORKDIR /app

COPY . .

# Build llama-cpp-python with CUDA
RUN pip3 install --no-cache-dir -r requirements.txt \
 && pip3 uninstall -y llama-cpp-python \
 && CMAKE_ARGS="-DLLAMA_CUDA=on" FORCE_CMAKE=1 pip3 install llama-cpp-python --no-cache-dir --force-reinstall

# Create model directory
RUN mkdir -p model

# Download the GGUF model using Hugging Face token
ARG HF_TOKEN
RUN mkdir -p model \
 && wget --header="Authorization: Bearer ${HF_TOKEN}" \
https://huggingface.co/lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct-Q8_0.gguf \
-O model/llama-3-8b-instruct-q8_0.gguf


EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
