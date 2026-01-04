#!/bin/bash
# run_vllm.sh
# Run this on GCP VM to start the vLLM server for Scenario A.

# Load HF_TOKEN from .env safely
export HF_TOKEN=$(uv run python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('HF_TOKEN', ''))")

if [ -z "$HF_TOKEN" ]; then
    echo "Warning: HF_TOKEN is empty. Gemma models might fail to load."
fi

MODEL=$(uv run python -c "import yaml; print(yaml.safe_load(open('config/config.yaml'))['model']['local_llm'])")

echo "Starting vLLM server with model: $MODEL"
echo "Ensure you have GPU enabled and 'vllm' installed."

# Run vLLM serving
# --dtype auto: Auto-detect float16/bfloat16
# --api-key EMPTY: No key required for local access
uv run vllm serve $MODEL --dtype auto --api-key EMPTY --port 32000