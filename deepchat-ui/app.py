from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
API_BASE = "http://127.0.0.1:8500"  # Your main API

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    r = requests.post(f"{API_BASE}/generate", json=data)
    return jsonify(r.json())

@app.route("/tasks", methods=["GET"])
def tasks():
    user_id = request.args.get("user_id", "")
    r = requests.get(f"{API_BASE}/history?user_id={user_id}")
    data = r.json()

    tasks = []
    if "history" in data and isinstance(data["history"], list):
        for item in data["history"]:
            if "task_name" in item and item["task_name"] not in tasks:
                tasks.append(item["task_name"])
    return jsonify({"tasks": tasks})

@app.route("/task-history", methods=["GET"])
def task_history():
    user_id = request.args.get("user_id", "")
    task_name = request.args.get("task_name", "")
    r = requests.get(f"{API_BASE}/history/task?user_id={user_id}&task_name={task_name}")
    return jsonify(r.json())

@app.route("/delete-task", methods=["DELETE"])
def delete_task():
    user_id = request.args.get("user_id", "")
    task_name = request.args.get("task_name", "")
    r = requests.delete(f"{API_BASE}/history/task?user_id={user_id}&task_name={task_name}")
    return jsonify(r.json())

@app.route("/delete-user", methods=["DELETE"])
def delete_user():
    user_id = request.args.get("user_id", "")
    r = requests.delete(f"{API_BASE}/history?user_id={user_id}")
    return jsonify(r.json())

if __name__ == "__main__":
    app.run(port=8600, debug=True)
