from flask import Flask, request, jsonify
from filters.filters import is_greeting
from message import get_greeting_response, get_decline_message
from querychecker import classify_text_with_deepseek
from ollama_client import query_ollama, split_message_and_code
from redis_client import save_history, get_all_history, clear_history
import json

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    user_id = data.get("user_id", "guest")

    if not prompt:
        return jsonify({"response": "⚠️ Please provide a prompt."})

    if is_greeting(prompt):
        return jsonify({"response": get_greeting_response()})

    # Classification
    classification = classify_text_with_deepseek(prompt)
    if classification != "Coding-related":
        retry = classify_text_with_deepseek(prompt) if classification == "Unclear" else classification
        if retry != "Coding-related":
            return jsonify({"response": get_decline_message()})

    # Fetch past conversation context
    history = get_all_history(user_id)
    context = ""
    for h in history:
        context += f"User: {h['prompt']}\nAssistant: {h['response']}\n"

    full_prompt = f"{context}User: {prompt}\nAssistant:"
    raw_response = query_ollama(full_prompt)
    structured = split_message_and_code(raw_response)

    save_history(user_id, prompt, structured.get("code") or structured.get("message"))

    return jsonify(structured)

@app.route("/history/<user_id>", methods=["GET"])
def view_history(user_id):
    history = get_all_history(user_id)
    if not history:
        return jsonify({"error": "No history found."}), 404
    return jsonify(history)

@app.route("/history/<user_id>", methods=["DELETE"])
def clear_user_history(user_id):
    deleted = clear_history(user_id)
    if deleted:
        return jsonify({"message": f"History cleared for {user_id}"}), 200
    return jsonify({"error": "No history to delete."}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5051)
