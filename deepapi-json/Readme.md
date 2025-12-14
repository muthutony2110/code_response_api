# Code Classification & Response API

This project is a **Flask-based API** that classifies user prompts as **coding-related or non-coding**, generates responses using an LLM (DeepSeek via Ollama), and stores conversation history **per user in JSON files**.

> Ollama is used to run the DeepSeek model **locally**, avoiding cloud APIs.  
> This ensures **data privacy, no API cost, and full control over the model**.

---

## Features

- ✅ Detects greetings (hi, hello, etc.)
- 🧠 Classifies prompts as coding / non-coding using DeepSeek
- 💻 Generates structured coding responses (`message` + `code`)
- 📁 Stores chat history in JSON files per `user_id`
- 🔁 Uses recent conversation history as context
- 🚫 Rejects non-programming questions

---

## Project Structure
