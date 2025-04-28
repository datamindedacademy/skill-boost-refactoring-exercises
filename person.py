import math
from abc import ABC, abstractmethod

from common import Experience


class PersonCalculator(ABC):
    @abstractmethod
    def calculate_volume_discount(self, days: int, experience: str) -> float:
        pass

    @abstractmethod
    def calculate_price(self, days: int, experience: str) -> float:
        pass


class TechnicalPersonCalculator(PersonCalculator):
    def calculate_volume_discount(self, days: int, experience: str) -> float:
        result = max(math.floor(days / 40), 0) * 500
        if experience == Experience.JUNIOR.value:
            result += math.floor(days / 20) * 500
        return result

    def calculate_price(self, days: int, experience: str) -> float:
        if experience == Experience.JUNIOR.value:
            base_fee = 500 * days
            if days <= 20:
                return base_fee
            return base_fee - (0.2 * (days - 20) * 500)
        elif experience == Experience.SENIOR.value:
            base_fee = 1000 * days
            if days <= 20:
                return base_fee
            return base_fee - (0.1 * (days - 20) * 1000)
        else:
            raise ValueError(f"unknown experience: {experience}")


class BusinessPersonCalculator(PersonCalculator):
    def calculate_volume_discount(self, days: int, experience: str) -> float:
        return 0.0

    def calculate_price(self, days: int, experience: str) -> float:
        return 1200 * days
