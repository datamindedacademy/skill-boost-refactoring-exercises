import locale
import math
from enum import Enum
from typing import Any

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

class Experience(Enum):
    JUNIOR = "junior"
    SENIOR = "senior"

def statement(monthly_invoice: dict, team_roles: dict) -> int:
    total_amount = 0
    volume_discount = 0
    result = f"Statement for {monthly_invoice['customer']}\n"

    for person in monthly_invoice['team']:
        role = team_roles[person['role']]
        this_amount = amount_for_person(person['days'], role['experience'])
        volume_discount += volume_discounts_for(person['days'], role['experience'])

        result += f" {person['role']}: {locale.currency(this_amount, grouping=True)} ({person['days']} days)\n"
        total_amount += this_amount

    result += f"Amount owed is {locale.currency(total_amount, grouping=True)}\n"
    result += f"You receive a volume discount: {locale.currency(volume_discount, grouping=True)} \n"

    return result


def volume_discounts_for(days: int, experience: str) -> int:
    result = 0
    result += max(math.floor(days / 40), 0) * 500
    if experience == Experience.JUNIOR.value:
        result += math.floor(days / 20) * 500
    return result


def amount_for_person(days: int, experience: str) -> int:
    result = 0
    if experience == Experience.JUNIOR.value:
        result = 500 * days
        if days > 20:
            result -= 0.2 * (days - 20) * 500
    elif experience == Experience.SENIOR.value:
        result = 1000 * days
        if days > 20:
            result -= 0.1 * (days - 20) * 1000
    else:
        raise ValueError(f"unknown experience level: {experience}")
    return result


def main():
    invoice = {
        "customer": "Gambit finance",
        "team": [
        {
            "role": "Team lead",
            "days": 20
        },
        {
            "role": "Associate engineer",
            "days": 40
        }]
    }
    roles = {
        "Associate engineer": {"type": "technical", "experience": "junior"},
        "Team lead": {"type": "technical", "experience": "senior"},
        "Customer success manager": {"type": "business", "experience": "senior"},
    }
    result = statement(invoice, roles)
    print(result)

if __name__ == "__main__":
    main()
