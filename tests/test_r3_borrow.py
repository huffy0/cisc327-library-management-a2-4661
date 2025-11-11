# tests/test_r3_borrow.py
import services.library_service as svc

def _add_and_get_book_id_by_isbn(isbn):
    ok, msg = svc.add_book_to_catalog("Dune", "Frank Herbert", isbn, 1)
    assert ok is True, f"add failed, message was: {msg}"
    row = svc.get_book_by_isbn(isbn)
    assert row is not None and isinstance(row, dict) and "id" in row, "get_book_by_isbn did not return a row with id"
    return row["id"]

def test_borrow_decrements_available():
    bid = _add_and_get_book_id_by_isbn("9780000000110")
    ok, msg = svc.borrow_book_by_patron("123456", bid)
    assert ok is True

def test_borrow_refuses_when_no_copies():
    bid = _add_and_get_book_id_by_isbn("9780000000111")
    svc.borrow_book_by_patron("123456", bid)
    ok, msg = svc.borrow_book_by_patron("000000", bid)
    assert ok is False

def test_borrow_requires_existing_book_id():
    ok, msg = svc.borrow_book_by_patron("123456", 99999999)
    assert ok is False

def test_borrow_requires_patron_id_format():
    bid = _add_and_get_book_id_by_isbn("9780000000112")
    ok, msg = svc.borrow_book_by_patron("", bid)
    assert ok is False
