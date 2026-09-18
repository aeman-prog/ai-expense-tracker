from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    amount: float
    description: str
    category: str
    date: str

class ExpenseUpdate(BaseModel):
    amount: float
    description: str
    category: str
    date: str