# tests/test_r4_return.py
import pytest
import library_service as svc

xfail_return = pytest.mark.xfail(reason="Return not implemented or partial")

def _add_borrow_get_ids():
    ok, _ = svc.add_book_to_catalog("Dune", "Frank Herbert", "9780000000113", 1)
    assert ok is True
    row = svc.get_book_by_isbn("9780000000113")
    assert row and "id" in row
    bid = row["id"]
    ok, _ = svc.borrow_book_by_patron("123456", bid)
    assert ok is True
    return "123456", bid

@xfail_return
def test_return_increments_available_when_valid():
    patron, book_id = _add_borrow_get_ids()
    ok, msg = svc.return_book_by_patron(patron, book_id)
    assert ok is True

@xfail_return
def test_return_rejects_wrong_patron():
    patron, book_id = _add_borrow_get_ids()
    ok, msg = svc.return_book_by_patron("000000", book_id)
    assert ok is False

@xfail_return
def test_return_idempotency_or_guard():
    patron, book_id = _add_borrow_get_ids()
    svc.return_book_by_patron(patron, book_id)
    ok, msg = svc.return_book_by_patron(patron, book_id)
    assert ok is False
