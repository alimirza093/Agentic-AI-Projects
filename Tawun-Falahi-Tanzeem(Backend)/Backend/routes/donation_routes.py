from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from validations.donation_validations import UserDonation
from utils.helping_func import verify_token
from config.database import get_db
from models.models import Donation

donation_router = APIRouter()

@donation_router.post("/")
def donate(donation: UserDonation, user = Depends(verify_token) , db=Depends(get_db)):
    try:
        user_id = user.get("user_id")
        username = user.get("username")
        new_donation = Donation(user_id=user_id, amount=donation.amount)
        db.add(new_donation)
        db.commit()
        db.refresh(new_donation)

        return {
            "message": "Donation successful",
            "data" : {
                "donation_id": new_donation.id,
                "username": username,
                "amount": new_donation.amount,
            },
            "status": "success"
    }
    except Exception as e:
        db.rollback()
        return {
            "message": "An error occurred while processing your donation",
            "error": str(e),
            "status": "error"
        }

@donation_router.get("/user/{user_id}")
def get_user_donations(user = Depends(verify_token), db=Depends(get_db)):
    try:
        user_id = user.get("user_id")
        donations = db.query(Donation).filter(Donation.user_id == user_id).all()
        if not donations:
            raise HTTPException(status_code=404, detail="No donations found for this user")
        total_amount = sum(donation.amount for donation in donations)
        return {
            "message": "User donations retrieved successfully",
            "data": {
                "user_id":  user_id,
                "username": user.get("username"),
                "total_amount": total_amount
            },
            "status": "success"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))