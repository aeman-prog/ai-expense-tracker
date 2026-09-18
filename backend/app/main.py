from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from . import models
from .schemas import ExpenseCreate, ExpenseUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "AI Expense Tracker API is running!"
    }


@app.post("/expenses")
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):
    new_expense = models.Expense(
        amount=expense.amount,
        description=expense.description,
        category=expense.category,
        date=expense.date
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense

@app.get("/expenses")
def get_expenses(
    db: Session = Depends(get_db)
    ):
    expenses = db.query(models.Expense).all()

    return expenses

@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id
    ).first()

    if expense is None:
        return {"message": "Expense not found"}

    return expense

@app.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    db: Session = Depends(get_db)
):
    existing_expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id
    ).first()

    if existing_expense is None:
        return {"message": "Expense not found"}

    existing_expense.amount = expense.amount
    existing_expense.description = expense.description
    existing_expense.category = expense.category
    existing_expense.date = expense.date

    db.commit()
    db.refresh(existing_expense)

    return existing_expense

@app.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id
    ).first()

    if expense is None:
        return {"message": "Expense not found"}

    db.delete(expense)
    db.commit()

    return {
        "message": "Expense deleted successfully"
    }