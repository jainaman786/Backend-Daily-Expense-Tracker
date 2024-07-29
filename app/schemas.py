from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    email: str
    name: str
    mobile_number: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class ExpenseParticipantsBase(BaseModel):
    user_id: int
    amount_owed: Optional[float] = None
    percentage: Optional[float] = None

class ExpenseParticipantsCreate(ExpenseParticipantsBase):
    pass

class ExpenseParticipants(ExpenseParticipantsBase):
    id: int

    class Config:
        orm_mode = True

class ExpenseBase(BaseModel):
    amount: float
    description: Optional[str] = None
    date: datetime
    split_method: str

class ExpenseCreate(ExpenseBase):
    participants: List[ExpenseParticipantsCreate]

class Expense(ExpenseBase):
    id: int
    participants: List[ExpenseParticipants] = []

    class Config:
        orm_mode = True
