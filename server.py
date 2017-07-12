from flask import Flask, render_template, request, redirect
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app, 'books')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_book():
    insert = 'insert into books (author, title, created_at) values(:author, :title, NOW())'
    data = {
        'author': request.form['author'],
        'title': request.form['title']  
    }
    mysql.query_db(insert, data)
    return redirect('/book_list')

@app.route('/book_list', methods=['GET', 'POST'])
def book_list():
    if request.method == 'POST':
        return redirect ('/book_list')
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
    delete = 'delete from books where id = :id'
    data = {'id': book_id}
    mysql.query_db(delete,data)
    return redirect ('/book_list')

@app.route('/update_book/<book_id>')
def update_book(book_id):
    query = 'select * from books where id = :id'
    data = {'id': book_id}
    book_info = mysql.query_db(query, data)
    book = book_info[0]
    return render_template ('update_book.html', book = book)

@app.route('/update_commit/<book_id>', methods = ["POST"])
def update_commit(book_id):
    update = 'update books set author = :author, title = :title, updated_at = NOW() where id = :id'
    data = {
        'author' : request.form['author'],
        'title' : request.form['title'],
        'id' : book_id
    }
    mysql.query_db(update, data)
    return redirect('/book_list')

@app.route('/add_quote/<book_id>')
def add_quote(book_id):
    query = 'select title, id from books where id = :id'
    data = {'id' : book_id}
    book_info = mysql.query_db(query, data)
    book = book_info[0]
    return render_template('add_quote.html', book=book)

@app.route('/quote_commit/<book_id>', methods = ["POST"])
def quote_commit(book_id):
    insert = 'insert into quotes (quote, created_at, book_id) values(:quote, NOW(), :book_id)'
    data = {
        'quote': request.form['quote'],
        'book_id': book_id
    }
    mysql.query_db(insert, data)
    return redirect('/quotes/' + book_id)

@app.route('/quotes/<book_id>')
def quotes(book_id):
    book_query = 'select title from books where id = :book_id'
    quote_query = 'select quote from quotes join books on book_id = books.id where book_id = :book_id'
    data = {'book_id': book_id}
    book_info = mysql.query_db(book_query, data)
    title = book_info[0]['title']
    all_quotes = mysql.query_db(quote_query, data)
    return render_template('quotes.html', all_quotes = all_quotes, title = title)

app.run(debug=True)