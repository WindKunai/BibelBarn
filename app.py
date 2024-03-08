from flask import Flask, render_template, request, jsonify, g, session, redirect, url_for, flash
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
    return render_template('index.html')

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

    return render_template('books.html', books=books)

@app.route('/save_order', methods=['POST'])
def save_order():
    order = request.form['order']
    # Save order data to the database
    # Implement your database logic here
    return jsonify({'message': 'Order saved successfully'})

@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

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

@app.route("/logout")
def logout():
    session.pop("username")
    session.pop("role")
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
