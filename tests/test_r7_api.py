# tests/test_r7_api.py
import pytest
import app as app_module

@pytest.fixture
def client():
    create_app = getattr(app_module, "create_app", None)
    assert create_app is not None, "create_app not found"
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_api_search_ok(client):
    r = client.get("/api/search?q=great&type=title")
    assert r.status_code in (200, 204)
    if r.status_code == 200:
        data = r.get_json()
        assert isinstance(data, dict)
        assert "results" in data
        assert isinstance(data["results"], list)

def test_api_late_fee_ok(client):
    r = client.get("/api/late_fee?patron_id=123456&book_id=1")
    assert r.status_code in (200, 400, 404)
