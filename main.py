import locale
import math
from typing import Any

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def statement(invoice: map, team_roles: map):
    total_amount = 0
    volume_discount = 0
    result = f"Statement for {invoice['customer']}\n"

    for person in invoice['team']:
        role = team_roles[person['role']]
        this_amount = amount_for_person(person['days'], role['experience'])
        volume_discount += volume_discounts_for(person['days'], role['experience'])

        result += f" {person['role']}: {locale.currency(this_amount, grouping=True)} ({person['days']} days)\n"
        total_amount += this_amount

    result += f"Amount owed is {locale.currency(total_amount, grouping=True)}\n"
    result += f"You receive a volume discount: {locale.currency(volume_discount, grouping=True)} \n"

    return result


def volume_discounts_for(days: int, experience: str):
    result = 0
    result += max(math.floor(days / 40), 0) * 500
    if experience == "junior":
        result += math.floor(days / 20) * 500
    return result


def amount_for_person(days: int, experience: str) -> int:
    result = 0
    if experience == "junior":
        result = 500 * days
        if days > 20:
            result -= 0.2 * (days - 20) * 500
    elif experience == "senior":
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
