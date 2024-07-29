from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .config import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    mobile_number = Column(String, nullable=False)

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    date = Column(DateTime, nullable=False)
    split_method = Column(String, nullable=False)
    participants = relationship('ExpenseParticipants', back_populates='expense')

class ExpenseParticipants(Base):
    __tablename__ = 'expense_participants'

    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey('expenses.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount_owed = Column(Float, nullable=False)
    expense = relationship('Expense', back_populates='participants')
