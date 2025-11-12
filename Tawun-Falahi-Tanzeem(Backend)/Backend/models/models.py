from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,Float, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
Base = declarative_base()

# Users Table
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now() , nullable=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now() , nullable=True)
    password = Column(String, nullable=False)

    donations = relationship("Donation", back_populates="user")
    loans = relationship("Loan", back_populates="user")
    fines = relationship("Fine", back_populates="user")
    installments = relationship("Installment", back_populates="user", cascade="all, delete-orphan")

# Donations Table
class Donation(Base):
    __tablename__ = 'donations'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    donated_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="donations")


# Loans Table
class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    installments = relationship("Installment", back_populates="loan", cascade="all, delete-orphan")
    fines = relationship("Fine", back_populates="loan", cascade="all, delete-orphan")
    user = relationship("User", back_populates="loans")


# Installments Table
class Installment(Base):
    __tablename__ = "installments"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey('loans.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(String, default="unpaid")
    paid_date = Column(DateTime, nullable=True)
    fine_amount = Column(Float, default=0.0) 
    total_amount = Column(Float, default=0.0)

    loan = relationship("Loan", back_populates="installments")
    user = relationship("User", back_populates="installments")


# Fines Table
class Fine(Base):
    __tablename__ = "fines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    loan_id = Column(Integer, ForeignKey('loans.id'))
    installment_id = Column(Integer, ForeignKey('installments.id'))
    fine_amount = Column(Float)
    days_late = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")
    
    user = relationship("User", back_populates="fines")
    loan = relationship("Loan", back_populates="fines")