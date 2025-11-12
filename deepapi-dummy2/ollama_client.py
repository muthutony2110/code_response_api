# File: ollama_client.py

import subprocess  # ✅ THIS IS REQUIRED

def query_ollama(prompt):
    final_prompt = f"""
You are a professional code assistant.

TASK:
Generate helpful, clean code or guidance based on the user prompt below.
Only respond with code and necessary explanations. Avoid filler phrases like "Sure!" or "Here's your code".

Prompt:
{prompt}
"""
    try:
        result = subprocess.run(
            ["ollama", "run", "deepseek-coder-v2:16b"],
            input=final_prompt.encode("utf-8"),
            capture_output=True,
            timeout=200
        )
        output = result.stdout.decode("utf-8").strip()
        return output or "⚠️ No response from DeepSeek."
    except subprocess.TimeoutExpired:
        return "⏰ DeepSeek took too long to respond. Try again."
    except Exception as e:
        return f"❌ Error calling DeepSeek: {str(e)}"
