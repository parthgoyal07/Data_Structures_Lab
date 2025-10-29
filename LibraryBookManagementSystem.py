# LIBRARY BOOK MANAGEMENT SYSTEM
Books = []        # LINKED LIST
Transactions = [] # STACK

# LINKED LIST FUNCTIONS

def INSERT(ID,TITLE,AUTHOR):
    Book = {"BookID": ID,"BookTitle": TITLE,"AuthorName": AUTHOR,"Status": "AVAILABLE!"}
    Books.append(Book)
    print("BOOK ADDED SUCCESSFULLY!")

def DELETE(ID):
    for B in Books:
        if B["BookID"] == ID:
            Books.remove(B)
            print(f"BOOK {ID} DELETED SUCCESSFULLY!")
            return
    print("BOOK NOT FOUND!")

def SEARCH(ID):
    for B in Books:
        if B["BookID"] == ID:
            print("BOOK FOUND:")
            print("Book ID:", B["BookID"])
            print("Title:", B["BookTitle"])
            print("Author:", B["AuthorName"])
            print("Status:", B["Status"])
            return
    print("BOOK NOT FOUND!")

def DISPLAY():
    if not Books:
        print("NO BOOKS IN THE LIBRARY!")
        return
    print("LIST OF BOOKS:")
    for B in Books:
        print(f"[{B['BookID']}] {B['BookTitle']} by {B['AuthorName']} ({B['Status']})")

# STACK FUNCTIONS

def ISSUE_BOOK(ID):
    for B in Books:
        if B["BookID"] == ID:
            if B["Status"] == "ISSUED!":
                print("BOOK ALREADY ISSUED!")
                return
            B["Status"] = "ISSUED!"
            Transactions.append(("ISSUE", ID))
            print(f"BOOK {B['BookTitle']} ISSUED SUCCESSFULLY!")
            return
    print("BOOK NOT FOUND!")

def RETURN_BOOK(ID):
    for B in Books:
        if B["BookID"] == ID:
            if B["Status"] == "AVAILABLE!":
                print("BOOK ALREADY AVAILABLE!")
                return
            B["Status"] = "AVAILABLE!"
            Transactions.append(("RETURN", ID))
            print(f"BOOK {B['BookTitle']} RETURNED SUCCESSFULLY!")
            return
    print("BOOK NOT FOUND!")

def UNDO():
    if not Transactions:
        print("NO TRANSACTIONS TO UNDO!")
        return
    ACTION,ID = Transactions.pop()
    for B in Books:
        if B["BookID"] == ID:
            if ACTION == "ISSUE":
                B["Status"] = "AVAILABLE!"
                print(f"UNDO: BOOK {B['BookTitle']} IS NOW AVAILABLE AGAIN.")
            elif ACTION == "RETURN":
                B["Status"] = "ISSUED!"
                print(f"UNDO: BOOK {B['BookTitle']} IS NOW ISSUED AGAIN.")
            return
        
def VIEW_TRANSACTIONS():
    if not Transactions:
        print("NO TRANSACTIONS RECORDED!")
        return
    print("TRANSACTION HISTORY:")
    for ACTION,ID in Transactions:
        print(f"{ACTION.title()} Book ID: {ID}")

# MAIN MENU

def MAIN():
    while True:
        print("===================================")
        print("    LIBRARY BOOK MANAGEMENT MENU    ")
        print("===================================")
        print("1. Insert New Book")
        print("2. Delete Book")
        print("3. Search Book")
        print("4. Display All Books")
        print("5. Issue Book")
        print("6. Return Book")
        print("7. Undo Last Transaction")
        print("8. View Transactions")
        print("9. Exit")
        print("===================================")

        CHOICE = input("Enter your choice: ")

        if CHOICE == "1":
            ID = int(input("Enter Book ID: "))
            TITLE = input("Enter Book Title: ")
            AUTHOR = input("Enter Author Name: ")
            INSERT(ID,TITLE,AUTHOR)
        elif CHOICE == "2":
            ID = int(input("Enter Book ID to delete: "))
            DELETE(ID)
        elif CHOICE == "3":
            ID = int(input("Enter Book ID to search: "))
            SEARCH(ID)
        elif CHOICE == "4":
            DISPLAY()
        elif CHOICE == "5":
            ID = int(input("Enter Book ID to issue: "))
            ISSUE_BOOK(ID)
        elif CHOICE == "6":
            ID = int(input("Enter Book ID to return: "))
            RETURN_BOOK(ID)
        elif CHOICE == "7":
            UNDO()
        elif CHOICE == "8":
            VIEW_TRANSACTIONS()
        elif CHOICE == "9":
            print("EXITING THE PROGRAM! .......")
            break
        else:
            print("INVALID CHOICE! PLEASE TRY AGAIN!")

# START THE PROGRAM
MAIN()