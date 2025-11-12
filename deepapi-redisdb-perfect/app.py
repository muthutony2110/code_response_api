from flask import Flask, request, jsonify
from filters.filters import is_greeting
from message import get_greeting_response, get_decline_message
from querychecker import classify_text_with_deepseek
from ollama_client import query_ollama, split_message_and_code
from redis_client import save_history, get_history, clear_history, get_all_history

app = Flask(__name__)


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    user_id = data.get("user_id", "guest")

    if not prompt:
        return jsonify({"response": "⚠️ Please provide a prompt."})

    # Check if prompt is a greeting
    if is_greeting(prompt):
        greeting = get_greeting_response()
        save_history(user_id, prompt, greeting)
        return jsonify({"response": greeting})

    # Classify if it's a coding-related prompt
    classification = classify_text_with_deepseek(prompt)
    print(f"[DEBUG] Classification Output: {classification}")

    if classification != "Coding-related":
        decline = get_decline_message()
        save_history(user_id, prompt, decline)
        return jsonify({"response": decline})

    # Get user history to build conversation context
    history = get_history(user_id, limit=6)
    context = ""
    for item in history:
        previous_response = item.get("response")
        if isinstance(previous_response, dict):
            message = previous_response.get("message", "")
        else:
            message = previous_response
        context += f"User: {item['prompt']}\nAssistant: {message}\n"

    # Combine current prompt with context
    full_prompt = f"{context}User: {prompt}\nAssistant:"

    # Call the model and extract structured response
    raw_response = query_ollama(full_prompt)
    structured = split_message_and_code(raw_response)

    # Save to Redis
    save_history(user_id, prompt, structured)
    return jsonify(structured)


@app.route("/history/<user_id>", methods=["GET"])
def view_history(user_id):
    history = get_all_history(user_id)
    if not history:
        return jsonify({"error": "No history found."}), 404
    return jsonify(history)


@app.route("/history/<user_id>", methods=["DELETE"])
def delete_history(user_id):
    result = clear_history(user_id)
    if result:
        return jsonify({"message": f"History cleared for {user_id}."})
    return jsonify({"error": "No history to delete."}), 404


if __name__ == '__main__':
    app.run(debug=True, port=8500)  # Changed port from 8000 to 8500
