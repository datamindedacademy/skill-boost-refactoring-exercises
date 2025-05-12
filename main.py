import locale
from typing import TypedDict, Collection, Mapping
from decimal import Decimal

# Set up US locale for currency formatting
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


ROLE_PRICING = {
    "junior": {"day_rate": Decimal("500"), "experience_discount": Decimal("20")},
    "senior": {"day_rate": Decimal("1000"), "experience_discount": Decimal("10")},
}
DAYS_AFTER_WHICH_EXPERIENCE_DISCOUNT_IS_APPLIED = 20


class TeamMember(TypedDict):
    role: str
    days: int


class Invoice(TypedDict):
    customer: str
    team: Collection[TeamMember]


class RoleInfo(TypedDict):
    type: str
    experience: str


class RolePricingInfo:
    def __init__(self, experience_level: str) -> None:
        if experience_level not in ROLE_PRICING:
            raise ValueError(f"unknown experience level: {experience_level}")
        role_data = ROLE_PRICING[experience_level]
        self.day_rate = role_data["day_rate"]
        self.experience_discount = role_data["experience_discount"] / 100
        self.experience_level = experience_level


class PersonWorkingForClient:
    def __init__(self, type: str, experience: str) -> None:
        self.type = type
        self.role_pricing_info = RolePricingInfo(experience_level=experience)

    def calculate_base_charge(self, days_charged: Decimal) -> Decimal:
        base_price = self.role_pricing_info.day_rate * days_charged
        exp_discount = self._calculate_exp_discount(days_charged)
        return base_price - exp_discount

    def calculate_total_discount(self, days_charged: Decimal) -> Decimal:
        volume_discount = self._calculate_volume_discount(days_charged)
        return volume_discount

    def _calculate_exp_discount(self, days_charged: Decimal) -> Decimal:
        if days_charged > DAYS_AFTER_WHICH_EXPERIENCE_DISCOUNT_IS_APPLIED:
            days_discounted = (
                days_charged - DAYS_AFTER_WHICH_EXPERIENCE_DISCOUNT_IS_APPLIED
            )
            return (
                self.role_pricing_info.experience_discount
                * days_discounted
                * self.role_pricing_info.day_rate
            )
        return Decimal(0)

    def _calculate_volume_discount(self, days_charged: Decimal) -> Decimal:
        volume_discount = (days_charged // 40) * Decimal("500")
        if self.role_pricing_info.experience_level == "junior":
            volume_discount += (days_charged // 20) * Decimal("500")
        return volume_discount


def statement(invoice: Invoice, role_mapping: Mapping[str, RoleInfo]) -> str:
    total_amount = Decimal("0")
    total_discount = Decimal("0")
    result = f"Statement for {invoice['customer']}\n"

    for member in invoice["team"]:
        role_info = role_mapping[member["role"]]
        days_worked = Decimal(member["days"])

        person = PersonWorkingForClient(
            type=role_info["type"], experience=role_info["experience"]
        )

        base_charge = person.calculate_base_charge(days_worked)
        discount = person.calculate_total_discount(days_worked)

        result += f" {member['role']}: {locale.currency(base_charge, grouping=True)} ({days_worked} days)\n"
        total_amount += base_charge
        total_discount += discount

    result += f"Amount owed is {locale.currency(total_amount, grouping=True)}\n"
    result += f"You receive a volume discount: {locale.currency(total_discount, grouping=True)}\n"
    return result


def main() -> None:
    invoice: Invoice = {
        "customer": "Gambit finance",
        "team": [
            {"role": "Team lead", "days": 20},
            {"role": "Associate engineer", "days": 40},
        ],
    }
    # Mapping of role title to role info
    role_mapping: Mapping[str, RoleInfo] = {
        "Associate engineer": {"type": "technical", "experience": "junior"},
        "Team lead": {"type": "technical", "experience": "senior"},
        "Customer success manager": {"type": "business", "experience": "senior"},
    }
    result = statement(invoice, role_mapping)
    print(result)


if __name__ == "__main__":
    main()
