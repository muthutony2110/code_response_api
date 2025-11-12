import subprocess
import re

def classify_text_with_deepseek(text):
    prompt = f"""
You are a classification AI.

INSTRUCTIONS:
Return ONLY "Yes" if the user's prompt is about software development, programming, coding, software, technology, or computer systems.
Return ONLY "No" if it is not.

Do not provide explanations.
Your answer must be "Yes" or "No".

Examples:
Prompt: "How do I write a Flask API in Python?" → Yes
Prompt: "What's the best place to visit in Paris?" → No
Prompt: "Create a C++ program for bubble sort" → Yes
Prompt: "Tell me a joke about cats" → No

Now classify the following:
Prompt: "{text}"
Answer:
"""
    try:
        result = subprocess.run(
            ["ollama", "run", "deepseek-coder-v2:16b"],
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=180
        )
        output = result.stdout.decode("utf-8").strip().lower()
        print("[DEBUG] Classification Output:", output)

        if "yes" in output:
            return "Coding-related"
        elif "no" in output:
            return "Not coding-related"
        else:
            return "Unclear"
    except subprocess.TimeoutExpired:
        return "Unclear"
    except Exception as e:
        return f"Error: {str(e)}"
