from decimal import Decimal

from pydantic import BaseModel, Field

from src.accounting.enums import TransactionType


class Account(BaseModel):
    account_id: int | None = Field(alias="id", default=None)
    name: str
    balance: Decimal


class Transaction(BaseModel):
    transaction_id: int | None = Field(alias="id", default=None)
    transaction_type: TransactionType = Field(alias="type")
    value: Decimal
    account_id: int
    category_id: int
    category_name: str
    category_icon: str
    description: str | None
    created_at: int


class Category(BaseModel):
    category_id: int | None = Field(alias="id", default=None)
    name: str
    icon: str
    parent_id: int | None = Field(default=None)
    is_income: bool
