import subprocess
import re

# Build prompt with clear instructions for the model
def build_prompt_with_context(history, prompt, task_name=None):
    base_instruction = (
        "You are a professional coding assistant.\n\n"
        f"You are continuing a conversation for the task: {task_name if task_name else 'General Task'}.\n"
        "Here is the previous conversation:\n\n"
    )

    context = ""
    for item in history:
        context += f"User: {item['prompt']}\nAssistant: {item['message']}\n"

    final_instruction = (
        "\nNow continue based on the new user input.\n"
        "TASK:\n"
        "- If the user asks for code, ALWAYS wrap the code inside triple backticks (```language ... ```).\n"
        "- Provide a short explanation first, then the full code.\n"
        "- If it's a conceptual or coding-related question, give a concise and clear answer.\n\n"
        "Respond ONLY if the topic is about programming or software development.\n\n"
    )

    return f"{base_instruction}{context}{final_instruction}User: {prompt}\nAssistant:"


# Query DeepSeek using Ollama CLI
def query_ollama(prompt):
    final_prompt = prompt
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

# Split message and code from the model's response
def split_message_and_code(response_text):
    if not response_text:
        return {"message": "⚠️ No response from model.", "code": ""}

    # Try extracting code between triple backticks
    code_match = re.search(r"```(?:[a-zA-Z]*\n)?(.*?)```", response_text, re.DOTALL)
    if code_match:
        return {
            "message": response_text.split("```")[0].strip(),
            "code": code_match.group(1).strip()
        }

    # Fallback: Assume first 3 lines are explanation, rest is code
    lines = response_text.splitlines()
    if len(lines) > 3:
        return {
            "message": "\n".join(lines[:3]).strip(),
            "code": "\n".join(lines[3:]).strip()
        }
    else:
        return {"message": response_text.strip(), "code": ""}
