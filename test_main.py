import pytest

from main import get_result, bank_file, hide_digit


def test_get_result():
    """Функция, которая тестирует get_result"""
    result = get_result(bank_file)
    assert type(result) is str
    assert len(result) != 0


def test_hide_digit():
    """Функция, которая тестирует hide_digit"""
    assert hide_digit("") == ""
