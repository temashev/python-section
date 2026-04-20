from src.wallets.exceptions import NegativeValueException, NotComparisonException
from src.wallets.currency import ALL_CURRENCIES

class Money:
    def __init__(self, value: int, currency: str):
        if value < 0:
            raise NegativeValueException('Сумма не может быть отрицательной')
        self.currency = currency
        self.value = value

    def __add__(self, other):
        """ Сложение """
        if self.currency != other.currency:
            raise NotComparisonException()
        return Money(self.value + other.value, self.currency)

    def __sub__(self, other):
        """ Вычитание """
        if self.currency != other.currency:
            raise NotComparisonException()
        return Money(self.value - other.value, self.currency)

    def __eq__(self, other):
        """ Равенство """
        return self.value == other.value and self.currency == other.currency


class Wallet:
    def __init__(self, initial_balance: Money=None):
        self._balance = dict.fromkeys(ALL_CURRENCIES, 0)

        if initial_balance:
            self.add(initial_balance)

    def add(self, money: Money):
        """ Пополнение кошелька """
        current_amount = self._balance.get(money.currency, 0)
        self._balance[money.currency] = current_amount + money.value
        return self

    def sub(self, money: Money):
        """ Снятие с кошелька """
        current_amount = self._balance.get(money.currency, 0)
        if current_amount < money.value:
            raise NegativeValueException('Недостаточно средств')

        self._balance[money.currency] = current_amount - money.value
        return self

    def get_balance(self, currency: ALL_CURRENCIES):
        return self._balance.get(currency, 0)
