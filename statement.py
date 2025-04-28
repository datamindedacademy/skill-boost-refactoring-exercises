import locale
from typing import List
from person import (
    PersonCalculator,
    TechnicalPersonCalculator,
    BusinessPersonCalculator,
    calculator_factory,
    Person,
)

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


class Statement:
    persons: List[Person]

    def __init__(self, customer: str):
        self.total_volume_discounts = 0.0
        self.total_cost = 0.0
        self.customer = customer
        self.persons = []

    def add_person(self, cost: float, role: str, experience: str, days: int):
        self.persons.append(Person(cost, role, experience, days))

    def add_total(self, total_cost: float):
        self.total_cost = total_cost

    def add_volume_discount(self, volume_discount: float):
        self.total_volume_discounts = volume_discount

    def format_total_cost(self):
        return locale.currency(self.total_cost, grouping=True)

    def format_volume_discount(self):
        return locale.currency(self.total_volume_discounts, grouping=True)


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


def create_statement(monthly_invoice: dict, team_roles: dict) -> Statement:
    statement = Statement(monthly_invoice["customer"])

    for person in get_team_from(monthly_invoice):
        role = team_roles[person["role"]]
        person_cost = amount_for_person(
            person["days"], experience_for(role), type_of_role(role)
        )
        statement.add_person(person_cost, role, experience_for(role), person["days"])

    invoice_amount = total_amount(get_team_from(monthly_invoice), team_roles)
    statement.add_total(invoice_amount)
    volume_discount = total_volume_discount(get_team_from(monthly_invoice), team_roles)
    statement.add_volume_discount(volume_discount)
    return statement


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


def get_team_from(monthly_invoice):
    return monthly_invoice["team"]


def experience_for(role):
    return role["experience"]


def type_of_role(role):
    return role["type"]
