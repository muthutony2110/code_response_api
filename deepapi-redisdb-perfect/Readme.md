# Code Classification & Response API

This project is a **Flask-based API** that classifies user prompts as **coding-related or non-coding**, generates responses using a **local LLM (DeepSeek via Ollama)**, and stores user conversation history in **Redis**.

Ollama is used to run LLM models **locally**, avoiding cloud APIs and ensuring **data privacy, no API cost, and full control over models**.

---

## Features

- ✅ Detects greetings (hi, hello, etc.)
- 🧠 Classifies prompts as coding / non-coding using DeepSeek
- 💻 Generates structured responses (`message` + `code`)
- 📦 Stores chat history per user in **Redis**
- 🔁 Uses recent conversation history as context
- 🚫 Rejects non-programming prompts
- 🖥️ Runs LLM models locally via Ollama

---

## Tech Stack

- **Backend:** Flask (Python)
- **LLM Runtime:** Ollama
- **Model:** DeepSeek Coder v2
- **Database:** Redis
- **Language:** Python 3.9+

---

## Project Structure

