from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class Ledger(Base):
    __tablename__ = "ledgers"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    createdAt = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        name="created_at",
    )
    updatedAt = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
        name="updated_at",
    )

    expenses = relationship("Expense", back_populates="ledger")


class ExpenseCategory(Base):
    __tablename__ = "expense_categories"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    createdAt = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        name="created_at",
    )
    updatedAt = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
        name="updated_at",
    )

    expenses = relationship("Expense", back_populates="category")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True)
    ledgerId = Column(String, ForeignKey("ledgers.id"), name="ledger_id")
    categoryId = Column(String, ForeignKey("expense_categories.id"), name="category_id")
    messageId = Column(String, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    payer = Column(String, nullable=False)
    createdAt = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        name="created_at",
    )
    updatedAt = Column(
        DateTime,
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
        name="updated_at",
    )

    ledger = relationship("Ledger", back_populates="expenses")
    category = relationship("ExpenseCategory", back_populates="expenses")

    __table_args__ = (UniqueConstraint("ledger_id", "messageId", name="_ledger_message_uc"),)
