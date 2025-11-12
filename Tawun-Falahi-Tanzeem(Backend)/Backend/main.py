from fastapi import FastAPI
from routes.user_routes import user_router  
from routes.donation_routes import donation_router
from routes.loan_routes import loan_router
app = FastAPI(debug=True)

app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(donation_router, prefix="/donation", tags=["Donation"])
app.include_router(loan_router, prefix="/loan", tags=["Loan"])

