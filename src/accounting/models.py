from decimal import Decimal

from pydantic import BaseModel, Field

from src.accounting.enums import TransactionType


class Account(BaseModel):
    account_id: int | None = Field(alias="id")
    name: str
    balance: Decimal


class Transaction(BaseModel):
    transaction_id: int | None = Field(alias="id")
    transaction_type: TransactionType = Field(alias="type")
    value: Decimal
    account_id: int
    description: str | None
    created_at: int
