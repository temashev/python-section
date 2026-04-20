from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Order:
    """There is no need to describe anything here."""
    price: float
    is_loyal: bool = False


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, current_price: float, order: Order) -> float:
        pass


class FixedDiscount(DiscountStrategy):
    """ Реализация фиксированной скидки в размере 200 р."""

    def __init__(self, discount_amount=200):
        self.discount_amount = discount_amount

    def apply(self, current_price: float, order: Order) -> float:
        if current_price >= 1000:
            return current_price - self.discount_amount
        return current_price


class LoyalDiscount(DiscountStrategy):
    """ Реализация скидки по карте лояльности в размере 20% от суммы заказа """

    def __init__(self, percentage=20):
        self.percentage = percentage

    def apply(self, current_price: float, order: Order) -> float:
        if order.is_loyal:
            return current_price * (1 - self.percentage / 100)
        return current_price


class PercentDiscount(DiscountStrategy):
    """ Процентная скидка на товары в размере 15% от суммы заказа """

    def __init__(self, percentage=15):
        self.percentage = percentage

    def apply(self, current_price: float, order: Order) -> float:
        return order.price * (1 - self.percentage / 100)


class DiscountCalculator:
    """ Расчет скидки """

    def __init__(self, strategies: list[DiscountStrategy]):
        self.strategies = strategies

    def calculate(self, order: Order) -> float:
        price = order.price
        for strategy in self.strategies:
            price = strategy.apply(price, order)
        return price
