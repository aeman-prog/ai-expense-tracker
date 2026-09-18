from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from .database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    date = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)