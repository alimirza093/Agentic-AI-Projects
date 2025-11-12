from pydantic import BaseModel, validator

class UserDonation(BaseModel):
    amount: float 

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be a positive number')
        if v < 300:
            raise ValueError('Amount must be at least 300')
        return v
