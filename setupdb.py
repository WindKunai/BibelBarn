import sqlite3

def create_database():
    conn = sqlite3.connect('BookLibrary.db')
    c = conn.cursor()

    # Create Users table
    c.execute('''CREATE TABLE IF NOT EXISTS Users
                 (UserID INTEGER PRIMARY KEY,
                 Username TEXT NOT NULL,
                 Password TEXT NOT NULL,
                 Email TEXT NOT NULL,
                 TotalBooksBorrowed INTEGER DEFAULT 0)''')

    # Create Books table
    c.execute(('''CREATE TABLE IF NOT EXISTS Books
                 (BookID INTEGER PRIMARY KEY,
                 BookName TEXT NOT NULL,
                 Author TEXT NOT NULL,
                 PublishingYear INTEGER,
                 Total INTEGER,
                 LentBooks INTEGER)'''))

    # Create Rentals table
    c.execute('''CREATE TABLE IF NOT EXISTS Rentals
                 (RentalID INTEGER PRIMARY KEY,
                 UserID INTEGER,
                 BookID INTEGER,
                 RentalDate DATE,
                 ReturnDate DATE,
                 FOREIGN KEY (UserID) REFERENCES Users(UserID),
                 FOREIGN KEY (BookID) REFERENCES Books(BookID))''')

    # Create BorrowHistory table
    c.execute('''CREATE TABLE IF NOT EXISTS BorrowHistory
                 (BorrowID INTEGER PRIMARY KEY,
                 UserID INTEGER,
                 Username TEXT,
                 BookID INTEGER,
                 BookName TEXT,
                 Date DATE,
                 Action TEXT,
                 FOREIGN KEY (UserID) REFERENCES Users(UserID),
                 FOREIGN KEY (BookID) REFERENCES Books(BookID))''')

    # Add example users
    users = [
        ('Alice', 'password1', 'alice@example.com'),
        ('Bob', 'password2', 'bob@example.com'),
        ('Charlie', 'password3', 'charlie@example.com'),
        ('Diana', 'password4', 'diana@example.com')
    ]
    c.executemany('INSERT INTO Users (Username, Password, Email) VALUES (?, ?, ?)', users)

    # Add example books
    books = [
        ('Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 1997, 5, 2),
        ('To Kill a Mockingbird', 'Harper Lee', 1960, 3, 1),
        ('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 4, 0),
        ('Pride and Prejudice', 'Jane Austen', 1813, 6, 3)
    ]
    c.executemany('INSERT INTO Books (BookName, Author, PublishingYear, Total, LentBooks) VALUES (?, ?, ?, ?, ?)', books)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()

