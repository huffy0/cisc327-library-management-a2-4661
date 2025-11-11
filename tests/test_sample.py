# sample_test.py
from services.library_service import add_book_to_catalog

def test_add_book_valid_input():
    ok, msg = add_book_to_catalog("Test Book Title", "Test Author Name", "9780000000101", 3)
    assert ok is True
