# File: ollama_client.py

import subprocess
import re

def query_ollama(prompt):
    # Updated system prompt
    final_prompt = f"""
You are a professional coding assistant.

TASK:
- If the user prompt is asking for code (e.g. HTML, CSS, Python, etc), provide the full code directly inside triple backticks (```).
- If the user is asking a programming-related conceptual question, explain it clearly.
- NEVER start with phrases like "Sure!" or "Here's your code".
- ONLY respond to software-related questions.

PROMPT:
{prompt}

Now respond clearly and professionally.
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "deepseek-coder-v2:16b"],
            input=final_prompt.encode("utf-8"),
            capture_output=True,
            timeout=200
        )
        response_text = result.stdout.decode("utf-8").strip()
        return split_message_and_code(response_text)

    except subprocess.TimeoutExpired:
        return {
            "message": "⏰ DeepSeek took too long to respond.",
            "code": ""
        }
    except Exception as e:
        return {
            "message": f"❌ Error calling DeepSeek: {str(e)}",
            "code": ""
        }

def split_message_and_code(response_text):
    if not response_text:
        return {"message": "⚠️ No response from DeepSeek.", "code": ""}

    # Attempt to extract code inside ```
    code_match = re.search(r"```(?:[a-zA-Z]*\n)?(.*?)```", response_text, re.DOTALL)

    if code_match:
        message_part = response_text.split("```")[0].strip()
        code_part = code_match.group(1).strip()

        return {
            "message": message_part if message_part else "✅ Here's your code.",
            "code": code_part
        }

    # Fallback: if no code block is detected, assume first 2-3 lines are heading
    lines = response_text.splitlines()
    if len(lines) <= 3:
        return {
            "message": response_text.strip(),
            "code": ""
        }
    
    return {
        "message": "\n".join(lines[:2]).strip(),
        "code": "\n".join(lines[2:]).strip()
    }
