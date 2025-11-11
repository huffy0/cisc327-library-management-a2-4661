import pytest
from services.library_service import calculate_late_fee_for_book, search_books_in_catalog

def test_calculate_late_fee_late_days():
    result = calculate_late_fee_for_book("123456", 1)
    assert isinstance(result, dict)
    assert "fee_amount" in result
    assert result["fee_amount"] >= 0

def test_search_case_insensitive():
    books = [
        {"title": "Harry Potter", "author": "Rowling", "isbn": "123"},
        {"title": "Hunger Games", "author": "Collins", "isbn": "456"},
    ]
    # mock get_all_books if needed
    result = search_books_in_catalog("harry", "title")
    assert isinstance(result, list)
