from fastapi import FastAPI
from typing import Optional , List
from pydantic import BaseModel, EmailStr, field_validator
import re


app = FastAPI()
class Student(BaseModel):
    name: str
    age: int 
    grade: bool = False
    email: EmailStr
    course : List[str]
    Phone_Number: Optional[int] = None
    address: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, name):
        if re.fullmatch(r"[A-Za-z]{1,50}", name):
            return name
        else:
            raise ValueError("Name should only contain alphabets and be less than 50 characters long")
    @field_validator("age")
    @classmethod    
    def validate_age(cls, age):
        if age >= 18 and age <= 50:
            return age
        else:
            raise ValueError("Age should be between 18 and 50")
    
    @field_validator("course")
    @classmethod    
    def validate_course(cls, course):
        if len(course) > 0 and len(course) < 6:
            return course
        else:
            raise ValueError("Course should be between 1 and 5")
    
    @field_validator("course")
    @classmethod
    def mul_course(cls, course):
        if len(course) == len(set(course)):
            return course
        else:
            raise ValueError("Course should be unique")

@app.post("/register/{student_id}")
  
  
async def register_student(student_id: int ,student : Student , grade : bool = False , semester: Optional[str] = None):
    try:    
        if student_id > 1000 and student_id < 9999:
            return {
                "student_Data" : {
                    "student_id": student_id,
                    "name": student.name,
                    "age": student.age,
                    "grade": grade,
                    "semester": semester,
                    "email" : student.email,
                    "course": student.course,
                    "Phone_Number": student.Phone_Number,
                    "address": student.address

                },
                "Message": "Student Registered Successfully",
                "Status": "Success"

            }
        else:
            raise Exception("Student ID should be between 1000 and 9999")    
            
    except Exception as e:
        return {
            "Message": str(e),
            "Status": "Failed",
            "Data" : None
        }


    