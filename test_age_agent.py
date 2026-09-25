import pytest

from age_agent import is_adult

def test_adult():
    assert is_adult(25) is True

def test_minor():
    assert is_adult(10) is False

def test_boundary_age():
    assert is_adult(18) is True

def test_negative_age():
    with pytest.raises(ValueError):
        is_adult(-1)