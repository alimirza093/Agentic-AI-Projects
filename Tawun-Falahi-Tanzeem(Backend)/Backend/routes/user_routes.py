from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from models.models import User
from utils.helping_func import create_access_token, hashed_password ,verify_password
from config.database import get_db
from validations.user_validations import UserLogin , UserSign
user_router = APIRouter()

@user_router.post("/signup")
def create_user(user: UserSign, db=Depends(get_db)):
    try:
        password = hashed_password(user.password)
        
        new_user = User(
            username=user.username,
            full_name=user.full_name,
            email=user.email,
            password=password,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        token = create_access_token(data={"user_id": new_user.id, "username": new_user.username})
        return JSONResponse(
            content={
                "message": "User created successfully",
                "user_id": new_user.id,
                "username": new_user.username,
                "token": str(token),
                "status": "success"
            },
            status_code=201
        )
    except Exception as e:
        db.rollback()
        return {
            "message": "Error creating user",
            "error": str(e),
            "status": "error"
        }
    
@user_router.post("/login")
def login_user(user: UserLogin, db=Depends(get_db)):
    try:

        existing_user = db.query(User).filter(User.email == user.email).first()

        if not existing_user:
            raise HTTPException(status_code=400, detail="user not found")
        # if hashed_password(user.password) != existing_user.password:
        #     raise HTTPException(status_code=400, detail="Incorrect password")
        authenticated_user = verify_password(user.password, existing_user.password)
        if not authenticated_user:
            raise HTTPException(status_code=400, detail="Incorrect password")

        token = create_access_token(data={
            "user_id": existing_user.id,
            "username": existing_user.username
        })

        return {
            "message": "Login successful",
            "token": str(token),
            "status": "success"
        }

    except Exception as e:
        return JSONResponse(
            content={
                "message": "Error logging in",
                "error": str(e),
                "status": "error"
            },
            status_code=500
        )
