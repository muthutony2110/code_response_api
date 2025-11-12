from flask import Flask, request, jsonify
from filters.filters import is_greeting
from message import get_greeting_response, get_decline_message
from querychecker import classify_text_with_deepseek
from ollama_client import query_ollama, split_message_and_code
from mssql_client import (
    save_history_with_task,
    get_history_by_task,
    get_all_user_history,
    delete_user_history,
    delete_task_history
)

app = Flask(__name__)


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()
        user_id = data.get("user_id", "guest").strip()
        task_name = data.get("task_name", "").strip()

        if not prompt or not task_name:
            return jsonify({
                "response": {
                    "message": "⚠️ Please provide both 'prompt' and 'task_name'.",
                    "code": ""
                }
            })

        if is_greeting(prompt):
            return jsonify({
                "response": {
                    "message": get_greeting_response(),
                    "code": ""
                }
            })

        classification = classify_text_with_deepseek(prompt)
        if classification == "Not coding-related":
            return jsonify({
                "response": {
                    "message": get_decline_message(),
                    "code": ""
                }
            })
        elif classification == "Unclear":
            return jsonify({
                "response": {
                    "message": "🤔 I'm not sure if it's about programming. Please clarify.",
                    "code": ""
                }
            })

        history = get_history_by_task(user_id, task_name, limit=3)
        context = ""
        for item in history:
            context += f"User: {item['prompt']}\nAssistant: {item['message']}\n"

        full_prompt = f"{context}User: {prompt}\nAssistant:"
        raw_response = query_ollama(full_prompt)
        structured = split_message_and_code(raw_response)

        save_history_with_task(user_id, task_name, prompt, structured['message'], structured['code'])

        return jsonify({"response": structured, "task_name": task_name})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "response": {
                "message": f"❌ Internal Server Error: {str(e)}",
                "code": ""
            }
        }), 500


@app.route("/history", methods=["GET"])
def get_user_history():
    user_id = request.args.get("user_id", "").strip()
    if not user_id:
        return jsonify({"error": "❗ Missing 'user_id' parameter."}), 400

    history = get_all_user_history(user_id)
    return jsonify({"user_id": user_id, "history": history})


@app.route("/history/task", methods=["GET"])
def get_user_task_history():
    user_id = request.args.get("user_id", "").strip()
    task_name = request.args.get("task_name", "").strip()

    if not user_id or not task_name:
        return jsonify({"error": "❗ Missing 'user_id' or 'task_name' parameter."}), 400

    history = get_history_by_task(user_id, task_name)
    return jsonify({"user_id": user_id, "task_name": task_name, "history": history})


@app.route("/history", methods=["DELETE"])
def delete_history_for_user():
    user_id = request.args.get("user_id", "").strip()
    if not user_id:
        return jsonify({"error": "❗ Missing 'user_id' parameter."}), 400

    delete_user_history(user_id)
    return jsonify({"message": f"✅ History deleted for user '{user_id}'."})


@app.route("/history/task", methods=["DELETE"])
def delete_task_history_for_user():
    user_id = request.args.get("user_id", "").strip()
    task_name = request.args.get("task_name", "").strip()

    if not user_id or not task_name:
        return jsonify({"error": "❗ Missing 'user_id' or 'task_name' parameter."}), 400

    delete_task_history(user_id, task_name)
    return jsonify({"message": f"✅ History deleted for user '{user_id}' and task '{task_name}'."})



if __name__ == "__main__":
    app.run(port=8500)
