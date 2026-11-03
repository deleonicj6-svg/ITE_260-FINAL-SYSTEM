from datetime import date, timedelta

# LIBRARIAN ACCOUNTS
librarians = {
    "deleon": "123",
    "fajardo": "456",
    "zach": "789"
}

current_librarian = ""

def librarian_login():
    global current_librarian

    while True:
        print("\n===== SELECT LIBRARIAN =====")
        print("1. deleon")
        print("2. fajardo")
        print("3. zach")
        print("4. Exit")

        choice = input("Select Librarian: ")

        if choice == "1":
            username = "deleon"
        elif choice == "2":
            username = "fajardo"
        elif choice == "3":
            username = "zach"
        elif choice == "4":
            print("Exiting system...")
            exit()
        else:
            print("Invalid choice!")
            continue

        password = input("Enter Password: ")

        if librarians[username] == password:
            current_librarian = username
            print(f"\nLogin Successful! Welcome Librarian {username}.")
            return
        else:
            print("Login Failed! Incorrect password.")
            
# LIBRARY MANAGEMENT SYSTEM

books = []

# HELPER: DISPLAY BOOKS IN A TABLE
def display_books_table(book_list):
    if not book_list:
        print("No books found.")
        return

    headers = ["Book ID", "Title", "Author", "Category", "Total", "Available", "Borrowed", "Status"]
    rows = []
    for book in book_list:
        status = "Available" if book["available"] > 0 else "Not Available"
        rows.append([
            book["id"], book["title"], book["author"], book.get("category", "Uncategorized"),
            str(book["copies"]), str(book["available"]),
            str(book["borrowed"]), status
        ])

    widths = [max(len(headers[i]), *(len(row[i]) for row in rows)) for i in range(len(headers))]
    line = "+-" + "-+-".join("-" * width for width in widths) + "-+"
    print(line)
    print("| " + " | ".join(headers[i].ljust(widths[i]) for i in range(len(headers))) + " |")
    print(line)
    for row in rows:
        print("| " + " | ".join(row[i].ljust(widths[i]) for i in range(len(headers))) + " |")
    print(line)


# 1. ADD BOOK
def add_book():
    print("\\n--- ADD BOOK ---")

    # Generate the next ID automatically (B001, B002, B003...)
    existing_numbers = []
    for book in books:
        book_id = book["id"]
        if book_id.startswith("B") and book_id[1:].isdigit():
            existing_numbers.append(int(book_id[1:]))
    next_number = max(existing_numbers, default=0) + 1
    book_id = f"B{next_number:03d}"

    print("Automatically Generated Book ID:", book_id)
    title = input("Enter Book Title: ").strip()
    author = input("Enter Author: ").strip()
    category = input("Enter Book Category (e.g., History, Science, Fiction): ").strip().title()
    if not category:
        category = "Uncategorized"

    while True:
        try:
            copies = int(input("Enter Number of Copies: "))
            if copies > 0:
                break
            print("Please enter a number greater than 0.")
        except ValueError:
            print("Please enter a valid number.")

    book = {
        "id": book_id,
        "title": title,
        "author": author,
        "category": category,
        "copies": copies,
        "available": copies,
        "borrowed": 0,
        "borrowers": []
    }
    books.append(book)
    print(f"Book added successfully! Book ID: {book_id}")
    print("Category:", category)
    print("Total Copies:", copies)


# 2. VIEW BOOKS
def view_books():
    print("\\n--- BOOKS GROUPED BY CATEGORY ---")
    if not books:
        print("No books found.")
        return

    categories = sorted({book.get("category", "Uncategorized") for book in books}, key=str.lower)
    for category in categories:
        print(f"\\n=== {category.upper()} ===")
        category_books = [book for book in books if book.get("category", "Uncategorized").lower() == category.lower()]
        display_books_table(category_books)


# 3. SEARCH BOOK
def search_book():
    print("\\n--- SEARCH BOOK ---")
    print("All books:")
    display_books_table(books)

    if not books:
        return

    keyword = input("\\nEnter Book ID, Title, Author, or Category to search: ").strip().lower()
    matches = [
        book for book in books
        if keyword in book["id"].lower()
        or keyword in book["title"].lower()
        or keyword in book["author"].lower()
        or keyword in book.get("category", "Uncategorized").lower()
    ]

    print("\\n--- SEARCH RESULTS GROUPED BY CATEGORY ---")
    if not matches:
        print("No books found matching your search.")
        return

    categories = sorted({book.get("category", "Uncategorized") for book in matches}, key=str.lower)
    for category in categories:
        print(f"\\n=== {category.upper()} ===")
        category_matches = [book for book in matches if book.get("category", "Uncategorized").lower() == category.lower()]
        display_books_table(category_matches)


# 4. BORROW BOOK
def borrow_book():
    print("\\n--- BORROW BOOK ---")
    if not books:
        print("No books available in the library.")
        return

    display_books_table(books)
    book_id = input("Enter Book ID to borrow: ").strip().upper()

    for book in books:
        if book["id"].upper() == book_id:
            if book["available"] == 0:
                print("Sorry, all copies of this book are borrowed.")
                return

            print("Book Title:", book["title"])
            print("Available Copies:", book["available"])

            while True:
                try:
                    pieces = int(input("Enter Number of Pieces to Borrow: "))
                    if 0 < pieces <= book["available"]:
                        break
                    elif pieces > book["available"]:
                        print("Not enough copies available.")
                    else:
                        print("Please enter a number greater than 0.")
                except ValueError:
                    print("Please enter a valid number.")

            borrower_id = input("Enter Borrower's ID: ").strip()
            borrower_name = input("Enter Borrower's Name: ").strip()
            borrow_date = date.today()
            due_date = borrow_date + timedelta(days=7)

            existing_borrower = None
            for borrower in book["borrowers"]:
                if (borrower.get("borrower_id", "").lower() == borrower_id.lower()
                        or borrower["name"].lower() == borrower_name.lower()):
                    existing_borrower = borrower
                    break

            if existing_borrower:
                existing_borrower["pieces"] += pieces
                existing_borrower["borrow_date"] = borrow_date
                existing_borrower["due_date"] = due_date
                existing_borrower["borrower_id"] = borrower_id
            else:
                book["borrowers"].append({
                    "borrower_id": borrower_id,
                    "name": borrower_name,
                    "pieces": pieces,
                    "borrow_date": borrow_date,
                    "due_date": due_date
                })

            book["available"] -= pieces
            book["borrowed"] += pieces

            print("\\nBook borrowed successfully!")
            print("Borrower ID:", borrower_id)
            print("Borrower:", borrower_name)
            print("Pieces Borrowed:", pieces)
            print("Borrow Date:", borrow_date.strftime("%B %d, %Y"))
            print("Due Date:", due_date.strftime("%B %d, %Y"))
            print("Return within 7 days.")
            return

    print("Book ID not found.")


# 5. RETURN BOOK
def return_book():
    print("\\n--- RETURN BOOK ---")
    borrower_lookup = input("Enter your Borrower's ID or Name: ").strip().lower()
    if not borrower_lookup:
        print("Please enter a Borrower's ID or Name.")
        return

    matches = []
    for book in books:
        for borrower in book["borrowers"]:
            if (borrower.get("borrower_id", "").lower() == borrower_lookup
                    or borrower["name"].lower() == borrower_lookup):
                matches.append((book, borrower))

    if not matches:
        print("No borrowed books found for that Borrower's ID or Name.")
        return

    print("\\n--- BOOKS BORROWED BY THIS BORROWER ---")
    headers = ["Book ID", "Title", "Borrower ID", "Borrower Name", "Pieces", "Borrow Date", "Due Date", "Status"]
    rows = []
    for book, borrower in matches:
        status = "OVERDUE" if date.today() > borrower["due_date"] else "On time"
        rows.append([
            book["id"], book["title"], borrower.get("borrower_id", "N/A"),
            borrower["name"], str(borrower["pieces"]),
            borrower["borrow_date"].strftime("%b %d, %Y"),
            borrower["due_date"].strftime("%b %d, %Y"), status
        ])

    widths = [max(len(headers[i]), *(len(row[i]) for row in rows)) for i in range(len(headers))]
    line = "+-" + "-+-".join("-" * width for width in widths) + "-+"
    print(line)
    print("| " + " | ".join(headers[i].ljust(widths[i]) for i in range(len(headers))) + " |")
    print(line)
    for row in rows:
        print("| " + " | ".join(row[i].ljust(widths[i]) for i in range(len(headers))) + " |")
    print(line)

    selected_id = input("\\nEnter the Book ID you want to return: ").strip().upper()
    selected = next(((book, borrower) for book, borrower in matches
                     if book["id"].upper() == selected_id), None)
    if not selected:
        print("That Book ID is not in this borrower's list.")
        return

    book, borrower = selected
    while True:
        try:
            pieces = int(input("Enter Number of Pieces to Return: "))
            if 0 < pieces <= borrower["pieces"]:
                break
            elif pieces > borrower["pieces"]:
                print("The borrower does not have that many pieces.")
            else:
                print("Please enter a number greater than 0.")
        except ValueError:
            print("Please enter a valid number.")

    borrower["pieces"] -= pieces
    book["available"] += pieces
    book["borrowed"] -= pieces

    if borrower["pieces"] == 0:
        book["borrowers"].remove(borrower)

    print("\\nBook returned successfully!")
    print("Pieces Returned:", pieces)
    print("Available Copies:", book["available"])
    print("Borrowed Copies:", book["borrowed"])


# 6. VIEW BORROWED BOOKS
def view_borrowed_books():
    print("\\n--- BORROWED BOOKS ---")
    rows = []
    for book in books:
        for borrower in book["borrowers"]:
            rows.append({
                "id": book["id"],
                "title": book["title"],
                "borrower_id": borrower.get("borrower_id", "N/A"),
                "name": borrower["name"],
                "pieces": str(borrower["pieces"]),
                "borrow_date": borrower["borrow_date"].strftime("%b %d, %Y"),
                "due_date": borrower["due_date"].strftime("%b %d, %Y")
            })

    if not rows:
        print("No books are currently borrowed.")
        return

    headers = ["Book ID", "Title", "Borrower ID", "Borrower Name", "Pieces", "Borrow Date", "Due Date"]
    values = [[r["id"], r["title"], r["borrower_id"], r["name"], r["pieces"], r["borrow_date"], r["due_date"]] for r in rows]
    widths = [max(len(headers[i]), *(len(row[i]) for row in values)) for i in range(len(headers))]
    line = "+-" + "-+-".join("-" * width for width in widths) + "-+"
    print(line)
    print("| " + " | ".join(headers[i].ljust(widths[i]) for i in range(len(headers))) + " |")
    print(line)
    for row in values:
        print("| " + " | ".join(row[i].ljust(widths[i]) for i in range(len(headers))) + " |")
    print(line)


# 7. UPDATE BOOK
def update_book():
    print("\n--- UPDATE BOOK ---")

    book_id = input("Enter Book ID: ")

    for book in books:

        if book["id"] == book_id:

            print("Current Title:", book["title"])
            print("Current Author:", book["author"])
            print("Current Category:", book.get("category", "Uncategorized"))
            print("Current Total Copies:", book["copies"])

            new_title = input(
                "Enter New Title "
                "(press Enter to keep current): "
            )

            new_author = input(
                "Enter New Author "
                "(press Enter to keep current): "
            )
            new_category = input(
                "Enter New Category (press Enter to keep current): "
            ).strip().title()

            if new_title != "":
                book["title"] = new_title

            if new_author != "":
                book["author"] = new_author
            if new_category != "":
                book["category"] = new_category

            # Update number of copies
            while True:

                new_copies = input(
                    "Enter New Number of Copies "
                    "(press Enter to keep current): "
                )

                if new_copies == "":
                    break

                try:
                    new_copies = int(new_copies)

                    if new_copies > 0:

                        if new_copies >= book["borrowed"]:

                            book["copies"] = new_copies
                            book["available"] = (
                                new_copies - book["borrowed"]
                            )

                            break

                        else:
                            print(
                                "Copies cannot be less than "
                                "the borrowed copies."
                            )

                    else:
                        print(
                            "Please enter a number greater than 0."
                        )

                except ValueError:
                    print("Please enter a valid number.")

            print("Book information updated successfully!")
            return

    print("Book ID not found.")

# 8. DELETE BOOK
def delete_book():
    print("\n--- DELETE BOOK ---")

    book_id = input("Enter Book ID: ")

    for book in books:

        if book["id"] == book_id:

            # Cannot delete if copies are borrowed
            if book["borrowed"] > 0:
                print(
                    "Cannot delete a book with borrowed copies."
                )
                return

            confirm = input(
                "Are you sure you want to delete this book? (Y/N): "
            )

            if confirm.lower() == "y":

                books.remove(book)

                print("Book deleted successfully!")

            else:
                print("Delete cancelled.")

            return

    print("Book ID not found.")


# MAIN MENU
def main():

    while True:

        print("\n==============================")
        print("   LIBRARY MANAGEMENT SYSTEM")
        print("==============================")
        print("1. Add Book")
        print("2. View Books")
        print("3. Search Book")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. View Borrowed Books")
        print("7. Update Book")
        print("8. Delete Book")
        print("9. Exit")
        print("==============================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book()

        elif choice == "2":
            view_books()

        elif choice == "3":
            search_book()

        elif choice == "4":
            borrow_book()

        elif choice == "5":
            return_book()

        elif choice == "6":
            view_borrowed_books()

        elif choice == "7":
            update_book()

        elif choice == "8":
            delete_book()

        elif choice == "9":
            print(
                "\nThank you for using the "
                "Library Management System!"
            )
            break

        else:
            print("Invalid choice. Please try again.")

# START PROGRAM
2
librarian_login()
3
main()