import sqlite3
import os


db_path = os.path.join(os.path.dirname(__file__), "library.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()



def initialize_db():
    cursor.execute("PRAGMA table_info(library)")
    columns = [col[1] for col in cursor.fetchall()]

    required_columns = [
        'book_id',
        'book_name',
        'author',
        'category',
        'borrower_name',
        'available'
    ]

   
    if columns and columns != required_columns:
        print("⚠ Old database detected. Fixing schema...")
        cursor.execute("DROP TABLE IF EXISTS library")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS library(
        book_id INTEGER PRIMARY KEY,
        book_name TEXT NOT NULL,
        author TEXT NOT NULL,
        category TEXT NOT NULL,
        borrower_name TEXT DEFAULT NULL,
        available INTEGER DEFAULT 1
    )
    """)

    conn.commit()


initialize_db()



def get_book_id():
    while True:
        try:
            return int(input("Enter Book ID: "))
        except ValueError:
            print(" Enter a valid NUMBER.\n")



def add_book():
    book_id = get_book_id()
    book_name = input("Enter Book Name: ").strip()
    author = input("Enter Author Name: ").strip()
    category = input("Enter Category: ").strip()

    try:
        cursor.execute("""
        INSERT INTO library
        (book_id, book_name, author, category)
        VALUES (?, ?, ?, ?)
        """, (book_id, book_name, author, category))

        conn.commit()
        print(" Book added successfully!\n")

    except sqlite3.IntegrityError:
        print(" Book ID already exists.\n")



def search_book():
    book_id = get_book_id()

    cursor.execute("SELECT * FROM library WHERE book_id=?", (book_id,))
    book = cursor.fetchone()

    if not book:
        print(" No book found with this ID.\n")
        return

    status = "Available " if book[5] else "Checked Out "

    print(f"""
BOOK DETAILS
ID        : {book[0]}
Name      : {book[1]}
Author    : {book[2]}
Category  : {book[3]}
Borrower  : {book[4]}
Status    : {status}
""")



def search_by_category():
    cat = input("Enter category: ").strip()

    cursor.execute("""
    SELECT * FROM library
    WHERE LOWER(category) = LOWER(?)
    """, (cat,))

    books = cursor.fetchall()

    if not books:
        print(" No books found in this category.\n")
        return

    print("\n Books Found:\n")

    for b in books:
        status = "Yes" if b[5] else "No"

        print(f"""
ID        : {b[0]}
Name      : {b[1]}
Author    : {b[2]}
Available : {status}
-------------------------
""")



def checkout_book():
    book_id = get_book_id()

    cursor.execute("SELECT available FROM library WHERE book_id=?", (book_id,))
    result = cursor.fetchone()

    if not result:
        print("Book does not exist.\n")
        return

    if result[0] == 0:
        print(" Book already checked out.\n")
        return

    borrower = input("Enter Borrower Name: ")

    cursor.execute("""
    UPDATE library
    SET borrower_name=?, available=0
    WHERE book_id=?
    """, (borrower, book_id))

    conn.commit()
    print("Checkout successful!\n")



def return_book():
    book_id = get_book_id()

    cursor.execute("SELECT available FROM library WHERE book_id=?", (book_id,))
    result = cursor.fetchone()

    if not result:
        print(" Book does not exist.\n")
        return

    if result[0] == 1:
        print(" Book already in library.\n")
        return

    cursor.execute("""
    UPDATE library
    SET borrower_name=NULL, available=1
    WHERE book_id=?
    """, (book_id,))

    conn.commit()
    print(" Book returned successfully!\n")



def view_books():
    cursor.execute("SELECT * FROM library")
    books = cursor.fetchall()

    if not books:
        print(" Library is empty.\n")
        return

    print("\n========= LIBRARY =========\n")

    for b in books:
        status = "Yes" if b[5] else "No"

        print(f"""
ID        : {b[0]}
Name      : {b[1]}
Author    : {b[2]}
Category  : {b[3]}
Borrower  : {b[4]}
Available : {status}
-------------------------
""")



while True:

    print("""
====== LIBRARY MANAGEMENT ======

1. Add Book
2. Search Book by ID
3. Search by Category
4. Checkout Book
5. Return Book
6. View All Books
7. Exit
""")

    choice = input("Enter choice: ")

    if choice == '1':
        add_book()

    elif choice == '2':
        search_book()

    elif choice == '3':
        search_by_category()

    elif choice == '4':
        checkout_book()

    elif choice == '5':
        return_book()

    elif choice == '6':
        view_books()

    elif choice == '7':
        conn.close()
        print(" Library Closed.")
        break

    else:
        print(" Invalid choice. Try again.\n")
