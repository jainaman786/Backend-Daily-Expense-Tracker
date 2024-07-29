from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models
from .config import SessionLocal
from fastapi.responses import FileResponse
from openpyxl import Workbook


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.post('/users', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(email=user.email, name=user.name, mobile_number=user.mobile_number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get('/users/{user_id}', response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@router.post('/expenses', response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    if expense.split_method == 'equal':
        amount_per_user = expense.amount / len(expense.participants)
        for participant in expense.participants:
            participant.amount_owed = amount_per_user
    elif expense.split_method == 'percentage':
        total_percentage = sum(p.percentage for p in expense.participants)
        if total_percentage != 100:
            raise HTTPException(status_code=400, detail='Percentages must add up to 100')
        for participant in expense.participants:
            participant.amount_owed = (expense.amount * participant.percentage) / 100
    elif expense.split_method == 'exact':
        total_exact = sum(p.amount_owed for p in expense.participants)
        if total_exact != expense.amount:
            raise HTTPException(status_code=400, detail='Exact amounts must sum up to the total expense')
    db_expense = models.Expense(
        amount=expense.amount,
        description=expense.description,
        date=expense.date,
        split_method=expense.split_method,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    for participant in expense.participants:
        db_participant = models.ExpenseParticipants(
            expense_id=db_expense.id,
            user_id=participant.user_id,
            amount_owed=participant.amount_owed,
        )
        db.add(db_participant)

    db.commit()
    return db_expense

@router.get('/expenses/user/{user_id}', response_model=list[schemas.ExpenseParticipants])
def get_user_expenses(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.ExpenseParticipants).filter(models.ExpenseParticipants.user_id == user_id).all()

@router.get('/expenses', response_model=list[schemas.Expense])
def get_all_expenses(db: Session = Depends(get_db)):
    return db.query(models.Expense).all()

@router.get('/expenses/overall', response_model=list[schemas.Expense])
def get_overall_expenses(db: Session = Depends(get_db)):
    return db.query(models.Expense).all()


@router.get('/balance-sheet/download', response_class=FileResponse)
def download_balance_sheet(db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).all()
    data = []
    for expense in expenses:
        for participant in expense.participants:
            data.append({
                'expense_id': expense.id,
                'description': expense.description,
                'date': expense.date,
                'amount': expense.amount,
                'split_method': expense.split_method,
                'user_id': participant.user_id,
                'amount_owed': participant.amount_owed,
            })
    
    wb = Workbook()
    ws = wb.active
    ws.append(['Expense ID', 'Description', 'Date', 'Amount', 'Split Method', 'User ID', 'Amount Owed'])
    
    for row in data:
        ws.append([row['expense_id'], row['description'], row['date'], row['amount'], row['split_method'], row['user_id'], row['amount_owed']])
    
    file_path = 'balance_sheet.xlsx'
    wb.save(file_path)
    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename='balance_sheet.xlsx')