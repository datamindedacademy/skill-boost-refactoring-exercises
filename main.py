import locale
import math
from enum import Enum
from typing import Any, List

from common import RoleType, Experience
from person import PersonCalculator, TechnicalPersonCalculator, BusinessPersonCalculator

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


def total_amount(team: List, team_roles: dict):
    result = 0
    for person in team:
        role = team_roles[person["role"]]
        result += amount_for_person(
            person["days"], experience_for(role), type_of_role(role)
        )
    return result


def total_volume_discount(team: List, team_roles: dict):
    result = 0
    for person in team:
        role = team_roles[person["role"]]
        result += volume_discounts_for(
            person["days"], experience_for(role), type_of_role(role)
        )
    return result


def calculate_invoice(monthly_invoice: dict, team_roles: dict) -> int:
    result = f"Statement for {monthly_invoice['customer']}\n"

    for person in get_team_from(monthly_invoice):
        role = team_roles[person["role"]]
        person_cost = amount_for_person(
            person["days"], experience_for(role), type_of_role(role)
        )
        result += f" {person['role']}: {locale.currency(person_cost, grouping=True)} ({person['days']} days)\n"

    invoice_amount = total_amount(get_team_from(monthly_invoice), team_roles)
    volume_discount = total_volume_discount(get_team_from(monthly_invoice), team_roles)
    result += f"Amount owed is {locale.currency(invoice_amount, grouping=True)}\n"
    result += f"You receive a volume discount: {locale.currency(volume_discount, grouping=True)} \n"

    return result


def volume_discounts_for(days: int, experience: str, role_type: str) -> int:
    result = 0
    calculator = calculator_factory(role_type)
    result += calculator.calculate_volume_discount(days, experience)
    return result


def amount_for_person(days: int, experience: str, role_type: str) -> int:
    result = 0
    calculator = calculator_factory(role_type)
    result += calculator.calculate_price(days, experience)
    return result


def calculator_factory(role_type: str) -> PersonCalculator:
    if role_type == RoleType.TECHNICAL.value:
        return TechnicalPersonCalculator()
    elif role_type == RoleType.BUSINESS.value:
        return BusinessPersonCalculator()
    else:
        raise ValueError(f"unknown role type: {role_type}")


def get_team_from(monthly_invoice):
    return monthly_invoice["team"]


def experience_for(role):
    return role["experience"]


def type_of_role(role):
    return role["type"]


def main():
    invoice = {
        "customer": "Gambit finance",
        "team": [
            {"role": "Team lead", "days": 20},
            {"role": "Associate engineer", "days": 40},
        ],
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
