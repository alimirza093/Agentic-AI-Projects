# 🎓 Student Result Management API

This is a simple CRUD API built with **FastAPI** and **MongoDB** to manage student exam results.  
It allows adding, viewing, updating, and deleting student results with grade calculation based on marks.

---

## 🚀 Features

- ➕ Add student result with automatic grade assignment
- 🔍 Get result by student name
- ✏️ Update student result by ID
- ❌ Delete student result by ID
- ✅ Grade calculated based on marks:
  - 90+ ➝ A
  - 80+ ➝ B
  - 70+ ➝ C
  - 60+ ➝ D
  - 50+ ➝ E
  - Below 50 ➝ F

---

## 📦 Requirements

fastapi
uvicorn
pymongo
python-dotenv
pydantic


Install via:

```bash
pip install -r requirements.txt


🛠 .env File Setup
Create a .env file in the same folder as the main script:

DB_URL=[Your DB_URL Here]
This file is used to securely load your MongoDB connection string.


▶️ How to Run
Activate virtual environment (optional but recommended)

Install requirements

pip install -r requirements.txt
Run FastAPI server


uvicorn your_file_name:app --reload

Open browser:
http://127.0.0.1:8000


Test in Swagger UI:
http://127.0.0.1:8000/docs


🧑‍💻 Author
Ali Mirza
Simple, clean, and functional FastAPI project for student records.