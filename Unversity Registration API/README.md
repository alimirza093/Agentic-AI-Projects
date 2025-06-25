# 🎓 University Registration API

This is a student registration API built using **FastAPI** and **Pydantic** for validation.  
It collects detailed student information and returns a structured response if all validations pass.

---

## 🚀 Features

- Accepts student registration data via POST request
- Validates:
  - Name: alphabets only (max 50 chars)
  - Age: must be between 18 and 50
  - Courses: between 1 to 5, and must be unique
- Supports optional fields: phone number, address, semester
- Validates student ID must be 4 digits (1000–9999)
- Uses modern Pydantic `field_validator`

---

## 📦 Requirements

```txt
fastapi
uvicorn
pydantic

Install them using
pip install -r requirements.txt
Create a requirements.txt file with the above lines if it doesn't exist.

▶️ How to Run
Clone or save the code in a file (e.g. main.py)

Open terminal and run:
uvicorn main:app --reload

Open your browser and visit:
http://127.0.0.1:8000/docs
You’ll see Swagger UI to test the API interactively.

📖 API Endpoint
📌 POST /register/{student_id}
Path Parameter:

student_id: (int) must be between 1000 and 9999

Body Parameters:

{
  "name": "Ali",
  "age": 21,
  "email": "ali@example.com",
  "course": ["Math", "Physics"],
  "Phone_Number": 1234567890,
  "address": "Lahore, Pakistan"
}

Query Parameters (Optional):
grade: bool (default: false)
semester: string (e.g. "Spring 2025")

✅ Example Success Response:
{
  "student_Data": {
    "student_id": 1234,
    "name": "Ali",
    "age": 21,
    "grade": false,
    "semester": "Fall 2025",
    "email": "ali@example.com",
    "course": ["Math", "Physics"],
    "Phone_Number": 1234567890,
    "address": "Lahore, Pakistan"
  },
  "Message": "Student Registered Successfully",
  "Status": "Success"
}


❌ Example Failure (Duplicate Course):
{
  "detail": [
    {
      "type": "value_error",
      "msg": "Course should be unique",
      "loc": ["body", "course"]
    }
  ]
}

🧑‍💻 Author
Ali Mirza
FastAPI enthusiast building practical, real-world API projects.