# tests/test_operations.py
from src.main import calculate_sum

def test_sum_positive():
    assert calculate_sum(1, 1) == 2

def test_sum_negative():
    assert calculate_sum(-1, -1) == -2