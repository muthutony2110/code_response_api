from flask import Flask, request, jsonify
from filters.filters import is_greeting
from message import get_greeting_response, get_decline_message
from querychecker import classify_text_with_deepseek
from ollama_client import query_ollama, split_message_and_code
from mssql_client import (
    save_history, get_history, get_all_history,
    delete_guest_history, delete_user_history,
    delete_specific_prompt
)

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()

        prompt = data.get("prompt", "").strip()
        user_id = data.get("user_id", "").strip()

        if not prompt:
            return jsonify({"error": "⚠️ 'prompt' is required."}), 400
        if not user_id:
            return jsonify({"error": "⚠️ 'user_id' is required."}), 400

        if is_greeting(prompt):
            return jsonify({"response": {"message": get_greeting_response(), "code": ""}})

        classification = classify_text_with_deepseek(prompt)
        if classification == "Not coding-related":
            return jsonify({"response": {"message": get_decline_message(), "code": ""}})
        elif classification == "Unclear":
            return jsonify({"response": {"message": "🤔 I'm not sure if it's about programming. Please clarify.", "code": ""}})

        history = get_history(user_id, limit=3)
        context = ""
        for item in history:
            context += f"User: {item['prompt']}\nAssistant: {item['message']}\n"

        full_prompt = f"{context}User: {prompt}\nAssistant:"
        raw_response = query_ollama(full_prompt)
        structured = split_message_and_code(raw_response)

        save_history(user_id, prompt, structured['message'], structured['code'])

        return jsonify({"response": structured})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"❌ Internal Server Error: {str(e)}"}), 500


@app.route("/history/<user_id>", methods=["GET"])
def user_history(user_id):
    try:
        return jsonify(get_history(user_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/history", methods=["GET"])
def all_history():
    try:
        return jsonify(get_all_history())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/history/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        delete_user_history(user_id)
        return jsonify({"message": f"✅ History cleared for user: {user_id}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/history/<user_id>/prompt", methods=["DELETE"])
def delete_prompt(user_id):
    try:
        data = request.get_json()
        prompt = data.get("prompt")
        if not prompt:
            return jsonify({"error": "⚠️ 'prompt' is required."}), 400
        delete_specific_prompt(user_id, prompt)
        return jsonify({"message": "✅ Prompt deleted successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=8500)
