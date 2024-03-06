from decimal import Decimal, InvalidOperation

from loguru import logger

from src.exceptions import InvalidAmountError


class BaseMoneyManager:
    @classmethod
    def validate_amount(cls, value: str | int | float) -> bool:
        try:
            Decimal(value)
        except InvalidOperation:
            return False
        else:
            return True

    @classmethod
    def convert_amount_to_decimal(cls, value: str | int | float) -> Decimal:  # type: ignore
        try:
            result = Decimal(value)
        except InvalidOperation as e:
            logger.error(e)
            raise InvalidAmountError()
        else:
            return result
