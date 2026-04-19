import pytest
from src.main import calculate_sum

def test_calculate_sum_basic():
    assert calculate_sum(5, 5) == 10

def test_calculate_sum_zero():
    assert calculate_sum(0, 0) == 0