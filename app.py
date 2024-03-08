from flask import Flask, render_template, request, jsonify, g, session, redirect, url_for, flash, session
import sqlite3
from setupdb import *
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.debug = True
app.secret_key = 'some_secret'

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    REMEBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict"
)
#TESTING WITH STAYING LOGGED IN WITHOUT CHECKIGN IT EACH TIME
def inject_user(file, books, borrow_history, books_to_deliver):
    if (borrow_history is not None) and (books_to_deliver is not None):
         return render_template(file, username="David", userID=1,borrow_history=borrow_history, books_to_deliver=books_to_deliver)
    if books is not None:
        return render_template(file, username="David", userID=1,books=books)
    return render_template(file, username="David", userID=1)


def get_db():
    if not hasattr(g, "_database"):
        print("create connection")
        g._database = sqlite3.connect("BookLibrary.db")
    return g._database

@app.teardown_appcontext
def teardown_db(error):
    db = getattr(g, "_database", None)
    if db is not None:
        print("close connection")
        db.close()

@app.route('/')
def index():
    #if session["username"]:
        #if session["username"][0] == "admin":
            return (inject_user("index.html", books=None, borrow_history=None, books_to_deliver=None))
            #return render_template('index.html', username="David", admin="admin", user_id=1)
        #else:
        #    return render_template('index.html', username=session["username"])
    #else:
     #   return render_template('index.html')

@app.route('/books')
def books():
    conn = sqlite3.connect('BookLibrary.db')
    c = conn.cursor()

    # Retrieve books with available amount
    c.execute('''SELECT BookID, BookName, Author, PublishingYear, 
                 (Total - IFNULL((SELECT COUNT(*) FROM Rentals WHERE BookID = Books.BookID), 0)) AS AvailableAmount
                 FROM Books''')
    books = c.fetchall()

    conn.close()

    return (inject_user("books.html", books=books, borrow_history=None, books_to_deliver=None))

@app.route('/save_order', methods=['POST'])
def save_order():
    order = request.form['order']
    # Save order data to the database
    # Implement your database logic here
    return jsonify({'message': 'Order saved successfully'})

@app.route('/rooms')
def rooms():
    return inject_user("rooms.html", books=None, borrow_history=None, books_to_deliver=None)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            db = get_db()
            name = request.form.get("username")
            user = get_user_by_name(db, name)
            if user:
                session["username"] = user["Username"]
                session["role"] = user["Role"]
            return redirect(url_for("index"))
        else:
            name = request.form.get("username")
            password = request.form.get("password")
            if not name or not password:
                flash("Username and/or Password cannot be empty")
            db = get_db()
            ok = add_user(db, name, generate_password_hash(password))
            if ok == -1:
                flash("Username alerady in use")
            return redirect(url_for("login"))
    return render_template('login.html')

@app.route('/tos')
def ToS():
    return render_template('ToS.html')


@app.route('/account/<int:UserID>')
def account(UserID):
    conn = sqlite3.connect('BookLibrary.db')
    c = conn.cursor()

    # Fetch transaction history (borrow history) for the user
    c.execute('''SELECT BookID, BookName, Date, Action FROM BorrowHistory WHERE UserID = ?''', (UserID,))
    borrow_history = c.fetchall()

    # Fetch books yet to be delivered for the user
    c.execute('''SELECT Rentals.BookID, Books.BookName, Rentals.RentalDate, Rentals.ReturnDate 
                 FROM Rentals 
                 JOIN Books ON Rentals.BookID = Books.BookID 
                 WHERE Rentals.UserID = ? AND Rentals.ReturnDate IS NULL''', (UserID,))
    books_to_deliver = c.fetchall()

    conn.close()
    return inject_user("account.html",None,borrow_history,books_to_deliver)
    #return render_template('account.html', borrow_history=borrow_history, books_to_deliver=books_to_deliver)

@app.route("/logout")
def logout():
    session.pop("username")
    session.pop("role")
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
