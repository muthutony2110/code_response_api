# Code Classification & Response API (SQL Server Version)

This project is a **Flask-based API** that classifies user prompts as **coding-related or non-coding**, generates responses using a **locally running LLM (DeepSeek via Ollama)**, and stores structured conversation history in **Microsoft SQL Server**.

Each conversation is tracked using both **user_id** and **task_name**, enabling task-wise context building and history retrieval.

Ollama is used to run LLM models **locally**, avoiding cloud APIs and ensuring **data privacy, zero API cost, and full control over model execution**.

---

## Key Features

- ✅ Greeting detection (hi, hello, etc.)
- 🧠 Prompt classification using DeepSeek (coding vs non-coding)
- 💻 Structured LLM responses (`message` + `code`)
- 🗂️ Task-based conversation grouping using `task_name`
- 🧾 Persistent chat history stored in **SQL Server**
- 🔁 Context-aware responses using task-specific history
- 🚫 Non-programming queries are rejected
- 🖥️ Fully local LLM execution via Ollama

---

## Tech Stack

- **Backend:** Flask (Python)
- **LLM Runtime:** Ollama
- **Model:** DeepSeek Coder v2 (16B)
- **Database:** Microsoft SQL Server
- **DB Connector:** pyodbc
- **Language:** Python 3.9+

---

## Project Structure

