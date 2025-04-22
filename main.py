import locale
import math
from enum import Enum
from typing import Any, List

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

class Experience(Enum):
    JUNIOR = "junior"
    SENIOR = "senior"

def total_amount(team: List, team_roles: dict):
    result = 0
    for person in team:
        role = team_roles[person['role']]
        result += amount_for_person(person['days'], experience_for(role))
    return result

def total_volume_discount(team: List, team_roles: dict):
    result = 0
    for person in team:
        role = team_roles[person['role']]
        result += volume_discounts_for(person['days'], experience_for(role))
    return result

def calculate_invoice(monthly_invoice: dict, team_roles: dict) -> int:
    result = f"Statement for {monthly_invoice['customer']}\n"

    for person in get_team_from(monthly_invoice):
        role = team_roles[person['role']]
        result += f" {person['role']}: {locale.currency(amount_for_person(person['days'], experience_for(role)), grouping=True)} ({person['days']} days)\n"

    invoice_amount = total_amount(get_team_from(monthly_invoice), team_roles)
    volume_discount = total_volume_discount(get_team_from(monthly_invoice), team_roles)
    result += f"Amount owed is {locale.currency(invoice_amount, grouping=True)}\n"
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

def get_team_from(monthly_invoice):
    return monthly_invoice['team']

def experience_for(role):
    return role['experience']

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
    result = calculate_invoice(invoice, roles)
    print(result)

if __name__ == "__main__":
    main()
