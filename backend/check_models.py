#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"API Key (first 20 chars): {api_key[:20]}...")

client = Anthropic(api_key=api_key)

# Try to list models or get model info
print("\nTrying to get model information...")

# Test with different model names
models_to_test = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307"
]

for model in models_to_test:
    try:
        # Try a simple message to see if model is accessible
        message = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print(f"✅ {model} - WORKS!")
        break
    except Exception as e:
        print(f"❌ {model} - {str(e)[:100]}")

