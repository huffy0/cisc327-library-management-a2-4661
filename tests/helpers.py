# tests/helpers.py
def seed_books(db, rows):
    sql = """INSERT INTO books(title, author, isbn, total_copies, available_copies)
             VALUES(?,?,?,?,?)"""
    db.executemany(sql, rows)
    db.commit()

def get_available(db, isbn):
    row = db.execute("SELECT available_copies FROM books WHERE isbn=?", (isbn,)).fetchone()
    return row["available_copies"] if row else None
