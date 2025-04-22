import pytest
from main import calculate_invoice, Experience


def test_statement():
    result = calculate_invoice({"customer": "test", "team": []}, {})

    assert "0.00" in result

def test_junior_engineer_1_month_amount():
    result = calculate_invoice({"customer": "test", "team": [{'role': 'engineer', 'days': 20}]}, {'engineer': {'experience': Experience.JUNIOR.value}})

    assert "10,000.00" in result

def test_engineer_unexisting_experience():
    with pytest.raises(ValueError):
        calculate_invoice({"customer": "test", "team": [{'role': 'engineer', 'days': 20}]}, {'engineer': {'experience': 'medior'}})

def test_two_junior_engineers_1_month_amount():
    result = calculate_invoice({"customer": "test", "team": [{'role': 'engineer', 'days': 40}]}, {'engineer': {'experience': Experience.JUNIOR.value}})

    assert "18,000.00" in result

def test_senior_engineer_1_month_amount():
    result = calculate_invoice({"customer": "test", "team": [{'role': 'engineer', 'days': 20}]}, {'engineer': {'experience': Experience.SENIOR.value}})

    assert "20,000.00" in result

def test_two_senior_engineers_1_month_amount():
    result = calculate_invoice({"customer": "test", "team": [{'role': 'engineer', 'days': 40}]}, {'engineer': {'experience': Experience.SENIOR.value}})

    assert "38,000.00" in result

def test_junior_engineer_1_month_extra_discount_500():
    result = calculate_invoice({"customer": "test", "team": [{'role': 'engineer', 'days': 20}]}, {'engineer': {'experience': Experience.JUNIOR.value}})

    assert "volume discount: $500.00" in result

def test_one_senior_engineer_1_month_extra_discount_0():
    result = calculate_invoice({"customer": "test", "team": [{'role': 'engineer', 'days': 20}]}, {'engineer': {'experience': Experience.SENIOR.value}})

    assert "volume discount: $0.00" in result

def test_two_junior_engineers_1_month_discount_500():
    result = calculate_invoice({"customer": "test", "team": [{'role': 'engineer', 'days': 40}]}, {'engineer': {'experience': Experience.JUNIOR.value}})

    assert "volume discount: $1,500.00" in result

def test_two_senior_engineer_1_month_extra_discount_500():
    result = calculate_invoice({"customer": "test", "team": [{'role': 'engineer', 'days': 40}]}, {'engineer': {'experience': Experience.SENIOR.value}})

    assert "volume discount: $500.00" in result