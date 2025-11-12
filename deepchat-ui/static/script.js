let selectedTask = "";

document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("load-tasks").addEventListener("click", loadTasks);
document.getElementById("delete-task").addEventListener("click", deleteTask);
document.getElementById("delete-user").addEventListener("click", deleteUser);
document.getElementById("new-task").addEventListener("click", newTask);

async function loadTasks(autoSelect = false) {
    const userId = document.getElementById("user-id").value.trim();
    if (!userId) return alert("Enter User ID.");
    const res = await fetch(`/tasks?user_id=${userId}`);
    const data = await res.json();
    const taskList = document.getElementById("task-list");
    taskList.innerHTML = "";

    if (data.tasks && data.tasks.length > 0) {
        data.tasks.forEach(taskName => {
            const li = document.createElement("li");
            li.textContent = taskName;
            if (taskName === selectedTask) li.classList.add("active");
            li.onclick = () => { selectedTask = taskName; highlightSelectedTask(); loadHistory(); };
            taskList.appendChild(li);
        });
        if (autoSelect && !selectedTask) {
            selectedTask = data.tasks[data.tasks.length - 1];
            highlightSelectedTask();
            loadHistory();
        }
    } else {
        taskList.innerHTML = "<li>No tasks found.</li>";
    }
}

async function loadHistory() {
    const userId = document.getElementById("user-id").value.trim();
    if (!userId || !selectedTask) return alert("Select a user and task.");
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = "Loading...";
    const res = await fetch(`/task-history?user_id=${userId}&task_name=${selectedTask}`);
    const data = await res.json();
    chatBox.innerHTML = "";
    if (data.history && data.history.length > 0) {
        data.history.forEach(item => {
            if (item.user_prompt) appendMessage("user", item.user_prompt);
            if (item.response_message) {
                let formatted = item.response_message;
                if (item.response_code) formatted += `<br><pre>${item.response_code}</pre>`;
                appendMessage("bot", formatted);
            }
        });
    } else {
        appendMessage("bot", "No messages found for this task.");
    }
}

async function sendMessage() {
    const userId = document.getElementById("user-id").value.trim();
    const input = document.getElementById("user-input");
    const prompt = input.value.trim();
    if (!userId) return alert("Enter User ID.");
    if (!selectedTask) selectedTask = "NewChat_" + Date.now();
    if (!prompt) return alert("Enter a message.");

    await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, task_name: selectedTask, prompt: prompt })
    });

    input.value = "";
    await loadTasks(true);
}

async function deleteTask() {
    const userId = document.getElementById("user-id").value.trim();
    if (!userId || !selectedTask) return alert("Select a user and task.");
    if (!confirm(`Delete task "${selectedTask}"?`)) return;
    await fetch(`/delete-task?user_id=${userId}&task_name=${selectedTask}`, { method: "DELETE" });
    selectedTask = "";
    document.getElementById("chat-box").innerHTML = "";
    await loadTasks();
}

async function deleteUser() {
    const userId = document.getElementById("user-id").value.trim();
    if (!userId) return alert("Enter User ID.");
    if (!confirm(`Delete ALL history for user "${userId}"?`)) return;
    await fetch(`/delete-user?user_id=${userId}`, { method: "DELETE" });
    selectedTask = "";
    document.getElementById("chat-box").innerHTML = "";
    document.getElementById("task-list").innerHTML = "";
}

function newTask() {
    selectedTask = "NewChat_" + Date.now();
    document.getElementById("chat-box").innerHTML = "";
    highlightSelectedTask();
}

function appendMessage(sender, text) {
    const chatBox = document.getElementById("chat-box");
    const div = document.createElement("div");
    div.className = "message " + sender;
    div.innerHTML = text.replace(/\n/g, "<br>");
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function highlightSelectedTask() {
    document.querySelectorAll("#task-list li").forEach(li => {
        li.classList.remove("active");
        if (li.textContent === selectedTask) li.classList.add("active");
    });
}
