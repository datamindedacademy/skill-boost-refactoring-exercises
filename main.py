import math
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def statement(invoice, roles):
    total_amount = 0
    volume_discount = 0
    result = f"Statement for {invoice['customer']}\n"

    for person in invoice['team']:
        role_info = roles[person['role']]
        experience = role_info['experience']
        days = person['days']

        amount = calculate_amount(experience, days)
        discount = calculate_volume_discount(experience, days)

        volume_discount += discount
        total_amount += amount

        result += format_line_item(person['role'], amount, days)

    result += f"Amount owed is {locale.currency(total_amount, grouping=True)}\n"
    result += f"You receive a volume discount: {locale.currency(volume_discount, grouping=True)} \n"

    return result

def calculate_amount(experience, days):
    if experience == "junior":
        rate = 500
        amount = rate * days
        if days > 20:
            amount -= 0.2 * (days - 20) * rate
    elif experience == "senior":
        rate = 1000
        amount = rate * days
        if days > 20:
            amount -= 0.1 * (days - 20) * rate
    else:
        raise ValueError(f"Unknown experience level: {experience}")
    return amount

def calculate_volume_discount(experience, days):
    discount = max(math.floor(days / 40), 0) * 500
    if experience == "junior":
        discount += math.floor(days / 20) * 500
    return discount

def format_line_item(role, amount, days):
    return f" {role}: {locale.currency(amount, grouping=True)} ({days} days)\n"


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
