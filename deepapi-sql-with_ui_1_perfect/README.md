# Code Response API – LLM-Based Coding Assistant

## 📌 Project Overview
The **Code Response API** is a lightweight **LLM-powered coding assistant** designed to answer **programming-related queries only**.  
Unlike general-purpose chatbots, this system is constrained to deliver **code-focused and developer-centric responses**, making it ideal for technical support, learning, and internal developer tooling.

The application integrates **local LLM execution via Ollama**, structured response generation, and **SQL-based conversation history storage**.

---

## 🎯 Objectives
- Build a coding-only AI assistant using LLMs  
- Restrict responses strictly to programming-related questions  
- Run LLM models **locally** without cloud APIs  
- Store user interaction history for session-based conversations  
- Expose functionality through a RESTful API  
- Validate API behavior using Postman and UI  

---

## 🛠️ Tech Stack

### Backend
- **Python 3.9+**
- **Flask** (REST API)
- **Ollama v0.x** (Local LLM runtime)
- **DeepSeek Coder v2 – 16B** (Code-specialized LLM)

### Database
- **Microsoft SQL Server (MSSQL)** – *current implementation*  
- Database layer is **SQL-agnostic** and can be adapted to MySQL / PostgreSQL

### Frontend
- **HTML / CSS**
- **Vanilla JavaScript** (UI integration)

### Testing & Tools
- **Postman** (API testing & validation)

---

## ⚙️ System Architecture
1. User submits a coding-related query via UI or API  
2. Flask backend validates and classifies the prompt  
3. Valid coding prompts are forwarded to **DeepSeek via Ollama**  
4. LLM generates a structured response (`message + code`)  
5. Query and response are stored in **SQL Server** with user & task context  
6. API returns the response to the client  

---

## 🔐 Key Features
- ✅ Coding-only response enforcement  
- ✅ Local LLM execution using Ollama (no cloud dependency)  
- ✅ RESTful API built with Flask  
- ✅ SQL Server integration for chat history  
- ✅ Task-based and user-based conversation tracking  
- ✅ API request/response validation using Postman  
- ✅ Simple web UI for interaction  

---

## 🧠 Why Ollama & DeepSeek Are Used
- **Ollama** enables running LLMs **locally**, ensuring data privacy, zero API cost, and offline capability.  
- **DeepSeek Coder v2 (16B)** is optimized for programming tasks, providing accurate and structured code responses.

---

## 🧪 API Testing
All endpoints were tested using **Postman** to ensure:
- Correct request payload handling  
- Proper response structure (`message` + `code`)  
- Rejection of non-programming queries  
- Successful database insertion and retrieval  

---

## 🧠 Use Cases
- Developer coding assistant  
- Internal learning tool for programmers  
- Controlled GenAI chatbot for technical teams  
- Foundation for enterprise GenAI applications  

---

## 🚀 Future Enhancements
- Authentication and user roles  
- Multi-language programming support  
- Code execution and validation  
- Improved UI/UX  
- Vector database integration for RAG-based context retrieval  

---

## 📌 Project Status
✅ Prototype completed  
✅ Backend, UI, and database integrated  
✅ API tested and validated  
✅ Ready for GitHub and portfolio showcase  

---

## 👤 Author
**Muthuraj M**  
AI & Machine Learning Engineer | Data Analyst  

📧 Email: maruthumuthu04@gmail.com  

---

## 📜 License
This project is developed for **learning, internal use, and portfolio purposes**.
