import locale
import math

# Set up US locale for currency formatting
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def statement(invoice, roles):
    total_amount = 0
    volume_discount = 0
    result = f"Statement for {invoice['customer']}\n"

    for pers in invoice['team']:
        role = roles[pers['role']]
        this_amount = 0

        if role['experience'] == "junior":
            this_amount = 500 * pers['days']
            if pers['days'] > 20:
                this_amount -= 0.2 * (pers['days'] - 20) * 500
        elif role['experience'] == "senior":
            this_amount = 1000 * pers['days']
            if pers['days'] > 20:
                this_amount -= 0.1 * (pers['audience'] - 20) * 1000
        else:
            raise ValueError(f"unknown experience level: {role['experience']}")

        # add volume discount
        volume_discount += max(math.floor(pers['days']/ 40), 0) * 500

        # extra credit for every junior engineer
        if role['experience'] == "junior":
            volume_discount += math.floor(pers['days'] / 20) * 500

        # print line for this order
        result += f" {pers['role']}: {locale.currency(this_amount, grouping=True)} ({pers['days']} days)\n"
        total_amount += this_amount

    result += f"Amount owed is {locale.currency(total_amount, grouping=True)}\n"
    result += f"You receive a volume discount: {locale.currency(volume_discount, grouping=True)} \n"

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
