from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

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

@app.route('/login')
def login():
    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)
