from flask import Flask, request, jsonify
from filters.filters import is_greeting
from message import get_greeting_response, get_decline_message
from querychecker import classify_text_with_deepseek
from ollama_client import query_ollama
import os, json

app = Flask(__name__)
history_folder = "user_logs"
os.makedirs(history_folder, exist_ok=True)

# 🔁 Load recent conversation history
def get_history(user_id, limit=3):
    path = os.path.join(history_folder, f"{user_id}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        history = json.load(f)
    return history[-limit:]

# 💾 Save conversation
def save_history(user_id, prompt, response):
    path = os.path.join(history_folder, f"{user_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    history.append({"prompt": prompt, "response": response})

    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    user_id = data.get("user_id", "guest")

    if not prompt:
        return jsonify({"response": {"message": "⚠️ Please provide a prompt.", "code": ""}})

    # Handle greetings like "hi", "hello", etc.
    if is_greeting(prompt):
        return jsonify({"response": {"message": get_greeting_response(), "code": ""}})

    # First attempt to classify
    classification = classify_text_with_deepseek(prompt)

    if classification == "Coding-related":
        print("[✅ DeepSeek classified as CODE prompt]")

        # Build context from history
        history = get_history(user_id, limit=3)
        context = ""
        for h in history:
            context += f"User: {h['prompt']}\nAssistant: {h['response'].get('message', '')}\n"

        full_prompt = f"{context}User: {prompt}\nAssistant:"
        structured = query_ollama(full_prompt)

        # Save to user history
        save_history(user_id, prompt, structured)
        return jsonify({"response": structured})

    elif classification == "Not coding-related":
        print("[❌ Rejected as non-code prompt]")
        return jsonify({"response": {"message": get_decline_message(), "code": ""}})

    else:
        # Retry once if unclear
        print("[⚠️ Classification unclear, retrying...]")
        retry = classify_text_with_deepseek(prompt)

        if retry == "Coding-related":
            print("[🔁 Retry classified as CODE prompt]")

            history = get_history(user_id, limit=3)
            context = ""
            for h in history:
                context += f"User: {h['prompt']}\nAssistant: {h['response'].get('message', '')}\n"

            full_prompt = f"{context}User: {prompt}\nAssistant:"
            structured = query_ollama(full_prompt)

            save_history(user_id, prompt, structured)
            return jsonify({"response": structured})

        elif retry == "Not coding-related":
            print("[🔁 Retry classified as NOT CODE]")
            return jsonify({"response": {"message": get_decline_message(), "code": ""}})
        else:
            print("[❓ Still unclear]")
            return jsonify({"response": {"message": "🤔 I'm not sure if your question is about programming. Please rephrase clearly.", "code": ""}})

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
