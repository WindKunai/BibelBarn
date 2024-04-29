import sqlite3
from sqlite3 import Error

def drop_tables(conn):
    c = conn.cursor()
    try:
        c.execute('''DROP TABLE Users''')
        c.execute('''DROP TABLE Books''')
        c.execute('''DROP TABLE Rentals''')
        c.execute('''DROP TABLE BorrowHistory''')
    except Error as err:
        print("Error: {}", format(err))
    else:
        print("Tables dropped.")
    finally:
        c.close()


def create_database():
    conn = sqlite3.connect('BookLibrary.db')
    c = conn.cursor()

    # Create Users table
    c.execute('''CREATE TABLE IF NOT EXISTS Users
                 (UserID INTEGER PRIMARY KEY,
                 Username TEXT UNIQUE NOT NULL,
                 Password TEXT NOT NULL,
                 Role TEXT,
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
        ('Alice', 'password1', 'alice@example.com', 'Admin'),
        ('Bob', 'password2', 'bob@example.com', 'User'),
        ('Charlie', 'password3', 'charlie@example.com', 'User'),
        ('Diana', 'password4', 'diana@example.com', 'User')
    ]
    c.executemany('INSERT INTO Users (Username, Password, Email, Role) VALUES (?, ?, ?, ?)', users)

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

def add_user(conn, username, password, email, role="user"):
    c = conn.cursor()
    try:
        sql = ("INSERT INTO Users (Username, Password, Email, Role) VALUES (?,?,?,?)")
        c.execute(sql, (username, password, email, role))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("User {} created with id {}.".format(username, c.lastrowid))
        return c.lastrowid
    finally:
        c.close()

def get_userid(conn, username):
    c = conn.cursor()
    try:
        sql = ("SELECT UserID FROM Users WHERE Username = ?")
        c.execute(sql, (username,))
        id = c.fetchone()
        if id:
            return id[0]
        else:
            return -1
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        c.close()
        
def get_user_by_name(conn, username):
    c = conn.cursor()
    try:
        sql = ("SELECT UserID, Username, Role FROM Users WHERE Username = ?")
        c.execute(sql, (username,))
        for row in c:
            (id, name, role) = row
            return {
                "Username": name,
                "UserID": id, 
                "Role": role
            }
        else:
            return {
                "Username": name,
                "UserID": None, 
                "Role": None
            }
    except sqlite3.Error as err:
        print("Error. {}".format(err))
    finally:
        c.close()

if __name__ == "__main__":
    conn = sqlite3.connect('BookLibrary.db')
    drop_tables(conn)
    create_database()

