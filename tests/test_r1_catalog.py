# tests/test_r1_catalog.py
import services.library_service as svc

def test_catalog_adds_two_distinct_books_with_unique_isbn():
    ok1, _ = svc.add_book_to_catalog("A Title", "B Author", "9780000000102", 1)
    ok2, _ = svc.add_book_to_catalog("C Title", "D Author", "9780000000103", 1)
    assert ok1 is True and ok2 is True
    r1 = svc.get_book_by_isbn("9780000000102")
    r2 = svc.get_book_by_isbn("9780000000103")
    assert r1 is not None and r2 is not None

def test_catalog_unique_isbn_enforced():
    svc.add_book_to_catalog("A Title", "B Author", "9780000000104", 1)
    ok, _ = svc.add_book_to_catalog("C Title", "D Author", "9780000000104", 1)
    assert ok is False

def test_catalog_items_have_required_fields():
    svc.add_book_to_catalog("X Title", "Y Author", "9780000000105", 1)
    row = svc.get_book_by_isbn("9780000000105")
    assert row is not None
    for key in ["id", "title", "author", "isbn"]:
        assert key in row
