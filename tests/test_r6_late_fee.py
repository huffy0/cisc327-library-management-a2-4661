# tests/test_r6_late_fee.py
import pytest
import library_service as svc

def _borrow_for_fee(isbn="9780000000119"):
    ok, msg = svc.add_book_to_catalog("Late Fee Book", "Author", isbn, 1)
    assert ok is True, f"add failed, message was: {msg}"
    row = svc.get_book_by_isbn(isbn)
    assert row and "id" in row
    book_id = row["id"]
    ok, _ = svc.borrow_book_by_patron("123456", book_id)
    assert ok is True
    return "123456", book_id

@pytest.mark.xfail(reason="calculate_late_fee_for_book returns None in starter code")
def test_fee_returns_dict_shape():
    patron, book_id = _borrow_for_fee("9780000000120")
    data = svc.calculate_late_fee_for_book(patron, book_id)
    assert isinstance(data, dict)
    assert len(data) >= 1
