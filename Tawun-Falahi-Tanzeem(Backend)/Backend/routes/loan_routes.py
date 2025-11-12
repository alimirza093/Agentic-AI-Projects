from fastapi import APIRouter, Depends, HTTPException
from dateutil.relativedelta import relativedelta
from datetime import datetime
from sqlalchemy import func
from validations.loan_validation import Userloan , Userpayloan
from config.database import get_db
from utils.helping_func import verify_token, check_user_eligibility
from models.models import Loan , Installment , Fine
loan_router = APIRouter()

@loan_router.post("/get-loan")
def get_loan(loan : Userloan,user = Depends(verify_token) , db = Depends(get_db)):
    try:
        user_id = user.get("user_id")
        user_eligibility = check_user_eligibility(user=user, db=db)
        if not user_eligibility:
            return{
                "status": "error",
                "message": "User is not eligible for a loan you have to donate for 6 months to be eligible for a loan"
            }
        else:
            existing_loan = db.query(Loan).filter(Loan.user_id == user_id).first()
            if existing_loan:
                return {
                    "status": "error",
                    "detail": "User already has an active loan"
                }
        amount = loan.amount
        new_loan = Loan(user_id=user_id, amount=amount)
        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)
        installment_amount = amount / 10
        start_date = new_loan.created_at
        installment = []
        for i in range(10):
            due_date = start_date + relativedelta(months=i+1) 
            installment_data = Installment(
                loan_id=new_loan.id,
                user_id=user_id,
                amount=installment_amount,
                due_date= due_date, 
                status="pending",
                fine_amount=0,
                total_amount=installment_amount  
            )
            installment.append(installment_data)
        db.add_all(installment)
        db.commit()


        return {
            "status": "success",
            "detail": "Loan successfully created",
            "loan_id": new_loan.id,
            "amount": new_loan.amount,
            "installments": [
                {
                    "installment_id": installment_data.id,
                    "amount": installment_data.amount,
                    "due_date": installment_data.due_date,
                    "status": installment_data.status
                } for installment_data in installment
            ]
        }
    except HTTPException as e:
        return{
            "message": "Error processing loan request",
            "status": "error",
            "detail": str(e.detail)
        }


@loan_router.post("/pay-loan")
def pay_loan(payloan : Userpayloan ,user = Depends(verify_token) , db = Depends(get_db)):
    try:
        user_id = user.get("user_id")
        today = datetime.utcnow()
        installments = db.query(Installment).filter(
            Installment.user_id == user_id,
            Installment.status == "pending",
            func.date_trunc('month', Installment.due_date) == func.date_trunc('month', today)
        ).first()
        if not installments:
            return {
                "status": "error",
                "message": "No pending installment found for this month"
            }
        if installments.status == "paid":
            return {
                "status": "error",
                "message": "Installment already paid"
            }
        
        # Fine Logic
        day_late = (today - installments.due_date).days
        fine_amount = max(0, day_late * 50)  
        installments.fine_amount = fine_amount
        installments.total_amount = installments.amount + fine_amount
        if fine_amount > 0:
            existing_fine = db.query(Fine).filter(
                Fine.user_id == user_id,
                Fine.installment_id == installments.id,
                Fine.status == "pending"
            ).first()
            if not existing_fine:
                fine = Fine(
                    user_id=user_id,
                    loan_id=installments.loan_id,
                    installment_id=installments.id,
                    fine_amount=fine_amount,
                    days_late=day_late,
                    status="pending",
                )
                db.add(fine)
        db.commit()
        to_pay = installments.total_amount
        pay_amount = payloan.amount
        if pay_amount < to_pay:
            return {
                "status": "error",
                "message": "Insufficient payment amount, please pay at least the total amount due",
                "installment Amount": installments.amount,
                "fine" : fine_amount,
                "Total Amount to pay": to_pay
            }
        fine = db.query(Fine).filter(
            Fine.user_id == user_id,
            Fine.installment_id == installments.id,
            Fine.status == "pending"
        ).first()
        if fine:
            fine.status = "paid"
            fine.paid_date = today
            db.commit() 
        installments.status = "paid"
        installments.paid_date = today
        db.commit()
        if pay_amount > to_pay:
            change = pay_amount - to_pay
            return {
                "status": "success",
                "message": "Installment paid successfully, change returned",
                "installment_id": installments.id,
                "fine_amount": fine_amount,
                "change_returned": change
            }
        return {
            "status": "success",
            "message": "Installment paid successfully",
            "installment_id": installments.id,
            "fine_amount": fine_amount
        }
    
    except HTTPException as e:
        return {
            "message": "Error processing payment",
            "status": "error",
            "detail": str(e.detail)
        }
