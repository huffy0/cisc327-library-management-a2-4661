CISC 327, Assignment 1
Name: Mo Yafeai
Student ID: 20324661

# Environment used
Windows 10, Python 3.12, pip 25.2
Virtual env at .venv, tested with pytest
How to run, .\.venv\Scripts\Activate.ps1, then pytest -q

# Project implementation status

| Functionality, requirement | Status, complete or partial | Evidence or notes |
|---|---|---|
| R1 Book catalog management, add book | Complete | add_book_to_catalog enforces title less than 200, author less than 100, ISBN exactly 13 digits, copies positive, duplicate ISBN rejected |
| R2 Add book validations | Complete | tests cover happy path, duplicate, zero copies, empty title |
| R3 Borrow a book | Complete | decrements available, blocks when none available, requires valid book id and patron id |
| R4 Return a book | Partial | return flow appears incomplete in starter code, tests are xfail |
| R5 Search | Partial | search returns empty for valid data, likely intentional bug, matching tests are xfail, shape tests still run |
| R6 Late fee | Partial | calculate_late_fee_for_book returns None in starter code, xfail for shape |
| R7 API endpoints | Complete | search returns wrapper dict with results, late fee endpoint returns status codes as expected |

# Unit test summary
Runner, pytest -q
All tests live in tests, common setup in tests/conftest.py
Each test uses a temp sqlite file, schema initialized automatically
Final local run, 16 passed, 4 xfailed, 2 xpassed

# How to reproduce locally
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
"@ | Out-File -Encoding utf8 A1_Yafeai_4661.md