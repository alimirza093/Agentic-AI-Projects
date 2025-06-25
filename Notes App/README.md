# 📝 Notepad App — FastAPI + MongoDB + Jinja2

A simple full-stack Notepad app built using **FastAPI** for the backend and **Jinja2 templates** for frontend rendering. This app allows users to create and manage notes stored in MongoDB, with a clean HTML UI and basic CSS styling.

---

## 🚀 Features

- Add, view, and delete notes
- Backend: FastAPI + PyMongo
- Frontend: Jinja2 templates + Custom CSS
- Environment-based DB config with `.env` file
- Fully modular code structure (routes, models, schemas)

---

## 📁 Project Folder Structure

Notepad-App/
│
├── Front-End/
│ ├── templates/
│ │ ├── index.html
│ │ └── notes.html
│ └── static/
│ ├── style.css
│ └── note.css
│
└── Back-End/
├── config/
│ └── db.py # MongoDB connection
├── models/
│ └── note_model.py # Note schema (PyMongo format)
├── routes/
│ └── note_routes.py # API routes (GET, POST, DELETE)
├── schema/
│ └── note_schema.py # Pydantic models (request validation)
├── index.py # FastAPI entry point
├── .env # MongoDB connection string (ignored in Git)
├── .gitignore # Ignore .env and other files
└── requirements.txt # Dependencies list


---

## ⚙️ .env File Format

App expects a `.env` file in `Back-End/` with the following:

DATABASE_URL=[Your URL Here]

Make sure it's listed in `.gitignore`:
`.env`


---

## 🔧 How to Run

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/notepad-app.git
cd Notepad-App/Back-End


Create Virtual Environment

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate


Install Requirements

pip install -r requirements.txt


Create .env file

Inside Back-End/


Run Server

uvicorn index:app --reload


Dependencies

fastapi
uvicorn
jinja2
pymongo
python-dotenv


Install with

pip install -r requirements.txt



🧑‍💻 Author
Ali Mirza
Made with ❤️ for learning FastAPI & full-stack development.


