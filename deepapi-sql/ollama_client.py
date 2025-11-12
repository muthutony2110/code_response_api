
import subprocess
import re

def query_ollama(prompt):
    final_prompt = f"""
You are a professional coding assistant.

TASK:
- If the user asks for code, provide the full code clearly.
- If the user asks a conceptual or coding-related question, give a short and clear explanation.

Respond ONLY if the topic is about programming or development.

Prompt: {prompt}
"""
    try:
        result = subprocess.run(
            ["ollama", "run", "deepseek-coder-v2:16b"],
            input=final_prompt.encode("utf-8"),
            capture_output=True,
            timeout=240
        )
        return result.stdout.decode("utf-8").strip()
    except subprocess.TimeoutExpired:
        return "⏰ DeepSeek took too long to respond."
    except Exception as e:
        return f"❌ Error calling DeepSeek: {str(e)}"

def split_message_and_code(response_text):
    if not response_text:
        return {"message": "⚠️ No response from model.", "code": ""}

    code_match = re.search(r"```(?:[a-zA-Z]*\n)?(.*?)```", response_text, re.DOTALL)

    if code_match:
        return {
            "message": response_text.split("```")[0].strip(),
            "code": code_match.group(1).strip()
        }

    lines = response_text.splitlines()
    return {
        "message": "\n".join(lines[:3]).strip(),
        "code": "\n".join(lines[3:]).strip()
    }