import pytest
from main import calculate_invoice, Experience


def test_statement():
    result = calculate_invoice({"customer": "test", "team": []}, {})

    assert "0.00" in result

def test_junior_engineer_1_month_amount():
    team_roles = create_team_role_engineer(Experience.JUNIOR)
    result = calculate_invoice({"customer": "test", "team": create_team_engineer(20)}, team_roles)

    assert "10,000.00" in result

def test_engineer_unexisting_experience():
    with pytest.raises(ValueError):
        calculate_invoice({"customer": "test", "team": create_team_engineer(20)}, {'engineer': {'experience': 'medior'}})

def test_two_junior_engineers_1_month_amount():
    team_roles = create_team_role_engineer(Experience.JUNIOR)
    result = calculate_invoice({"customer": "test", "team": create_team_engineer(40)}, team_roles)

    assert "18,000.00" in result

def test_senior_engineer_1_month_amount():
    team_roles = create_team_role_engineer(Experience.SENIOR)
    result = calculate_invoice({"customer": "test", "team": create_team_engineer(20)}, team_roles)

    assert "20,000.00" in result

def test_two_senior_engineers_1_month_amount():
    team_roles = create_team_role_engineer(Experience.SENIOR)
    result = calculate_invoice({"customer": "test", "team": create_team_engineer(40)}, team_roles)

    assert "38,000.00" in result

def test_junior_engineer_1_month_extra_discount_500():
    team_roles = create_team_role_engineer(Experience.JUNIOR)
    result = calculate_invoice({"customer": "test", "team":create_team_engineer(20)}, team_roles)

    assert "volume discount: $500.00" in result

def test_one_senior_engineer_1_month_extra_discount_0():
    team_roles = create_team_role_engineer(Experience.SENIOR)
    result = calculate_invoice({"customer": "test", "team": create_team_engineer(20)}, team_roles)

    assert "volume discount: $0.00" in result

def test_two_junior_engineers_1_month_discount_500():
    team_roles = create_team_role_engineer(Experience.JUNIOR)
    result = calculate_invoice({"customer": "test", "team": create_team_engineer(40)}, team_roles)

    assert "volume discount: $1,500.00" in result

def test_two_senior_engineer_1_month_extra_discount_500():
    team_roles = create_team_role_engineer(Experience.SENIOR)
    result = calculate_invoice({"customer": "test", "team": create_team_engineer(40)}, team_roles)

    assert "volume discount: $500.00" in result

def create_team_engineer(days: int):
    return [{'role': 'engineer', 'days': days}]

def create_team_role_engineer(experience: Experience):
    return {'engineer': {'experience': experience.value}}