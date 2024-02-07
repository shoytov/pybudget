from decimal import Decimal

from pydantic import BaseModel, Field

from src.accounting.enums import TransactionType


class Account(BaseModel):
    _id: int = Field(alias="id")
    name: str
    balance: Decimal


class Transaction(BaseModel):
    _id: int = Field(alias="id")
    _type: TransactionType = Field(alias="type")
    value: Decimal
    account_id: int
    description: str | None
    created_at: int
