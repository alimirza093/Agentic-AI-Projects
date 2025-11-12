from pydantic import BaseModel, validator

class Userloan(BaseModel):
    amount: int

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v < 1000:
            raise ValueError('Loan amount must be at least 1000')
        if v > 10000:
            raise ValueError('Loan amount must not exceed 10000')
        if v % 100 != 0:
            raise ValueError('Loan amount must be a multiple of 100')
        if v < 0:
            raise ValueError('Loan amount must be positive')
        return v
    
class Userpayloan(BaseModel):
        amount: int 

        @validator('amount')
        def amount_must_be_positive(cls, v):
            if v <= 0:
                raise ValueError('Payment amount must be positive')
            return v