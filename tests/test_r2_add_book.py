# tests/test_r2_add_book.py
import library_service as svc

def test_add_book_happy_path():
    ok, msg = svc.add_book_to_catalog("Clean Code", "Robert Martin", "9780000000106", 3)
    assert ok is True

def test_add_book_rejects_duplicate_isbn():
    svc.add_book_to_catalog("X", "Y", "9780000000107", 2)
    ok, msg = svc.add_book_to_catalog("Other", "Auth", "9780000000107", 1)
    assert ok is False

def test_add_book_requires_positive_total_copies():
    ok, msg = svc.add_book_to_catalog("Bad", "Auth", "9780000000108", 0)
    assert ok is False

def test_add_book_requires_nonempty_fields():
    ok, msg = svc.add_book_to_catalog("", "Auth", "9780000000109", 1)
    assert ok is False
