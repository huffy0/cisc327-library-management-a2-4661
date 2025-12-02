from playwright.sync_api import Page, expect
import time

BASE_URL = "http://localhost:5000"


def test_add_book_and_borrow_flow(page: Page):
    """
    End to end flow:
    1. Open Add Book page
    2. Add a new book
    3. Verify it appears in the catalog
    4. Borrow that book from the catalog table
    5. Verify we are still on the catalog page and the book is listed
    """

    # Make the title and ISBN unique
    suffix = str(int(time.time_ns()))[-5:]
    title = f"E2E Test Book {suffix}"
    isbn = ("1234567890" + suffix)[-13:]  # keep 13 digits

    # 1. Go to Add Book page
    page.goto(f"{BASE_URL}/add_book")

    # 2. Fill and submit the Add Book form
    page.fill("input[name='title']", title)
    page.fill("input[name='author']", "E2E Author")
    page.fill("input[name='isbn']", isbn)
    page.fill("input[name='total_copies']", "3")

    page.click("button[type='submit']")

    # Confirm we are back on the catalog page and the new title appears
    body = page.locator("body")
    expect(body).to_contain_text("Book Catalog")
    expect(body).to_contain_text(title)

    # 3. Find the table row for our new book
    row = page.locator("tbody tr", has_text=title).first
    expect(row).to_contain_text("E2E Author")
    expect(row).to_contain_text(isbn)

    # 4. Fill the patron id in that same row and click Borrow
    row.locator("input[name='patron_id']").fill("123456")
    row.locator("button.btn.btn-success").click()

    # 5. Simple post condition: still on catalog and book still listed
    expect(page.locator("body")).to_contain_text("Book Catalog")
    expect(page.locator("body")).to_contain_text(title)


def test_sample_e2e(page: Page):
    page.goto(BASE_URL)
    expect(page).to_have_title("Library Management System")
