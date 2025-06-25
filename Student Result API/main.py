from fastapi import FastAPI
from pydantic import BaseModel , field_validator
from pymongo import MongoClient 
from bson import ObjectId 
from dotenv import load_dotenv
import os
class Result(BaseModel):
    student_name: str
    subject: str
    marks: int
    # grade: str

    @field_validator("marks")
    @classmethod
    def validate_marks(cls, marks):
        if 0 <= marks <= 100:
            return marks
        else:
            raise ValueError("Marks should be between 0 and 100")
try:
    load_dotenv()  
    db_url = os.getenv("DB_URL")
    client = MongoClient(db_url)
    db = client["Student-Result"]
    collection = db["Result"]
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Server is running"}
@app.post("/add-result/")
def add_result(result: Result):
    try:
        if(result.marks >= 90):
            grade = "A"
        elif(result.marks >= 80):
            grade = "B"
        elif(result.marks >= 70):
            grade = "C"
        elif(result.marks >= 60):
            grade = "D"
        elif(result.marks >= 50):
            grade = "E"
        else:
            grade = "F"
        resultData = {
                "student_name": result.student_name,
                "subject": result.subject,
                "marks": result.marks,
                "grade": grade
            }
        inserted = collection.insert_one(resultData)
        resultData["_id"] = str(inserted.inserted_id)        
        return {
            "message": "Result added successfully",
            "data": resultData,
            "Status": "Success"
            }
    except Exception as e:
        return {
            "message": "Error adding result",
            "error": str(e),
            "Status": "Failed",
            "data": []
        }
    
@app.get("/get-result/{student_name}")
def get_result(student_name: str):
    try:
        results = collection.find_one({"student_name": student_name})
        if results:
            results["_id"] = str(results["_id"])
            data = {
                "student_name": results["student_name"],
                "subject": results["subject"],
                "marks": results["marks"],
                "grade": results["grade"]
            }
            return {
                "message": "Results retrieved successfully",
                "data": data,
                "Status": "Success"
            }
        else:
            return {
                "message": "No results found for the given student name",
                "data": [],
                "Status": "Failed"
            }
    except Exception as e:
        return {
            "message": "Error retrieving results",
            "error": str(e),
            "Status": "Failed",
            "data": []
        }
@app.put("/update-result/")
def update_result(result: Result, student_id: str):
    try:
        if result.marks >= 90:
            grade = "A"
        elif result.marks >= 80:
            grade = "B"
        elif result.marks >= 70:
            grade = "C"
        elif result.marks >= 60:
            grade = "D"
        elif result.marks >= 50:
            grade = "E"
        else:
            grade = "F"

        resultData = {
            "student_name": result.student_name,
            "subject": result.subject,
            "marks": result.marks,
            "grade": grade
        }

        result_update = collection.update_one(
            {"_id": ObjectId(student_id)},
            {"$set": resultData}
        )

        if result_update.matched_count == 0:
            return {
                "message": "No matching record found with given ID",
                "data": [],
                "Status": "Failed"
            }

        return {
            "message": "Result updated successfully",
            "data": resultData,
            "Status": "Success"
        }

    except Exception as e:
        return {
            "message": "Error updating result",
            "error": str(e),
            "Status": "Failed",
            "data": []
        }
@app.delete("/delete-result/{student_id}")
def delete_result(student_id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(student_id)})
        if result.deleted_count == 0:
            return {
                "message": "No matching record found with given ID",
                "data": [],
                "Status": "Failed"
            }
        return {
            "message": "Result deleted successfully",
            "data": [],
            "Status": "Success"
        }
    except Exception as e:
        return {
            "message": "Error deleting result",
            "error": str(e),
            "Status": "Failed",
            "data": []
        }