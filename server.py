from flask import Flask, render_template, request, redirect
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app, 'books')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_book():
    query = 'insert into books (author, title, created_at) values(:author, :title, NOW())'
    data = {
        'author': request.form['author'],
        'title': request.form['title']  
    }
    mysql.query_db(query, data)
    return redirect('/book_list')

@app.route('/book_list')
def book_list():
    query = 'select author, title, date_format(created_at, "%b %D %Y") as date_added, id from books'
    all_books = mysql.query_db(query)
    return render_template ('book_list.html', all_books = all_books)

@app.route('/delete_confirm/<book_id>')
def delete_confirm(book_id):
    query = 'select * from books where id = :id'
    data = {'id': book_id}
    book_info = mysql.query_db(query, data)
    book = book_info[0]
    return render_template ('delete_book.html', book = book)

@app.route('/delete/<book_id>')
def delete(book_id):
    query = 'delete from books where id = :id'
    data = {'id': book_id}
    mysql.query_db(query,data)
    return redirect ('/book_list')

app.run(debug=True)