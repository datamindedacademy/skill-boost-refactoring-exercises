from statement import create_statement, Statement


def calculate_plain_text_invoice(monthly_invoice: dict, team_roles: dict) -> str:
    statement = create_statement(monthly_invoice, team_roles)
    result = render_plain_text(statement)
    return result


def calculate_html_invoice(monthly_invoice: dict, team_roles: dict) -> str:
    statement = create_statement(monthly_invoice, team_roles)
    result = render_html(statement)
    return result


def render_plain_text(statement: Statement):
    result = f"Statement for {statement.customer}\n"
    for person in statement.persons:
        result += f" {person.role}: {person.format_cost()} ({person.days} days)\n"
    result += f"Amount owed is {statement.format_total_cost()}\n"
    result += f"On top you receive a volume discount of {statement.format_volume_discount()} \n"
    return result


def render_html(statement: Statement) -> str:
    result = f"<h1>Statement for {statement.customer}</h1>\n"
    result += "<table>\n"
    result += "<tr><th>Role</th><th>Days</th><th>Cost</th></tr>\n"
    for person in statement.persons:
        result += f"<tr><td>{person.role}</td><td>{person.days}</td><td>{person.cost}</td></tr>\n"

    result += "</table>\n"

    result += f"<p>Amount owed is <em>{statement.format_total_cost()}</em></p>\n"
    result += f"<p>On top you receive a volume discount of <em>{statement.format_volume_discount()}</em> </p>\n"
    return result


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
    result = calculate_html_invoice(invoice, roles)
    print(result)


if __name__ == "__main__":
    main()
