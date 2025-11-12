from flask import Flask, request, jsonify
from filters.filters import is_greeting
from message import get_greeting_response, get_decline_message
from ollama_client import query_ollama
import os
import json
import re

app = Flask(__name__)
history_folder = "user_logs"
os.makedirs(history_folder, exist_ok=True)


def get_history(user_id, limit=3):
    path = os.path.join(history_folder, f"{user_id}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        history = json.load(f)
    return history[-limit:]


def save_history(user_id, prompt, structured_response):
    path = os.path.join(history_folder, f"{user_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    history.append({
        "prompt": prompt,
        "response": structured_response
    })

    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def split_message_and_code(response_text):
    """
    Extracts the heading/message and code block separately from LLM output.
    """
    # Try to split message and code
    code_match = re.search(r"```[a-zA-Z]*\n(.*?)```", response_text, re.DOTALL)

    if code_match:
        code = code_match.group(1).strip()
        message = response_text.split("```")[0].strip()
    else:
        # fallback if no code block found
        message = response_text.strip()
        code = ""

    return {"message": message, "code": code}


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    user_id = data.get("user_id", "guest")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    if is_greeting(prompt):
        structured = {
            "message": get_greeting_response(),
            "code": ""
        }
    else:
        # Load previous history
        history = get_history(user_id, limit=3)
        context = "### Instruction:\nYou are a helpful coding assistant. Continue the following conversation.\n\n### Conversation:\n"
        for h in history:
            prev = h["response"]
            context += f"User: {h['prompt']}\nAssistant: {prev['message']}\n"
            if prev["code"]:
                context += f"{prev['code']}\n"
        full_prompt = f"{context}User: {prompt}\nAssistant:"

        # Query DeepSeek
        raw_response = query_ollama(full_prompt)

        if not raw_response or "Error" in raw_response:
            structured = {
                "message": get_decline_message(),
                "code": ""
            }
        else:
            structured = split_message_and_code(raw_response)

    # Save structured history
    save_history(user_id, prompt, structured)
    return jsonify(structured)


@app.route("/history/<user_id>", methods=["GET"])
def view_history(user_id):
    path = os.path.join(history_folder, f"{user_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify({"error": "No history found."}), 404


@app.route("/history/<user_id>", methods=["DELETE"])
def clear_history(user_id):
    path = os.path.join(history_folder, f"{user_id}.json")
    if os.path.exists(path):
        os.remove(path)
        return jsonify({"message": f"History cleared for {user_id}"}), 200
    return jsonify({"error": "No history to delete."}), 404


if __name__ == '__main__':
    app.run(debug=True, port=8000)
