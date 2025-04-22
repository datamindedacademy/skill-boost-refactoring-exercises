import pytest
from main import statement

def test_statement():
    result = statement({"customer":"test", "team": []}, {})

    assert "0.00" in result
