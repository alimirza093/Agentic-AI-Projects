from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends , HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import func
from config.database import get_db
from models.models import Donation
import os
import jwt
from passlib.context import CryptContext

# Load .env from the project tree reliably
load_dotenv(find_dotenv())

oAuth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300
if not SECRET_KEY:
    # Provide a clearer runtime-safe error so callers don't get a confusing jwt exception
    raise ValueError("SECRET_KEY is not set in the environment variables. Please set SECRET_KEY in your .env file or environment.")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt





def verify_token(token: str = Depends(oAuth2_scheme)):
    try:
        decoded_token = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM],
    options={"require": ["exp"]},  # verify_exp default True hota hai
    leeway=60  # 60 seconds ka leeway dena
)
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def check_user_eligibility(user = Depends(verify_token), db=Depends(get_db)):
    user_id = user.get("user_id")
    result = db.query(
        func.date_trunc('month', Donation.donated_at).label("month")
    ).filter(
        Donation.user_id == user_id
    ).distinct().count()
    if result >= 6:
        return True 
    else:
        return False
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hashed_password(password):
    try:
        hashed = pwd_context.hash(password)
        return hashed
    except Exception as e:
        raise e
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)