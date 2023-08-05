from flask import Flask, render_template, request, redirect, url_for

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import sqlite3

#db =  sqlite3.connect('database.db')

#cursor = db.cursor()

# una volta creato il codice qua sotto non serve più perchè ogni volta che viene richiamato crea sempre un nuovo doc sql che non puà essere modificato
#cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")

#cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
#db.commit()
#qua sopra si è usato sql3 classico, come comefare la stessa cosa usando sql alchemy? = procedimento qua sotto


db=SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db.init_app(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)

with app.app_context():
    db.create_all()

def add_book(title,author,rating):
    new_book = Books(title=title, author=author,rating=rating)
    db.session.add(new_book)
    db.session.commit()



    '''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''



all_books = []




@app.route('/')
def home():
    with app.app_context():
        # books = db.session.query(Books).all()

        users = db.session.execute(db.select(Books).order_by(Books.title)).scalars()

        # Print the books
        # for book in books:
        #     print(book.id, book.title, book.author, book.rating)

        return render_template('index.html', books=users)


@app.route("/add" ,methods=['GET',"POST"])
def add():
    if request.method == 'POST':
        book = request.form['book name']
        author = request.form['book author']
        rating = float(request.form['rating'])

        with app.app_context():
            new_book = Books(title=book, author=author, rating=rating)
            db.session.add(new_book)
            db.session.commit()

        #
        # new_book = {
        #     'name': book,
        #     'author': author,
        #     'rating': rating
        # }
        # all_books.append(new_book)
        # print(all_books)

    return render_template('add.html')

@app.route("/edit/<el>", methods=['GET', 'POST'])
def edit_rating(el):
    if request.method == 'POST':
        rating1= request.form['new_rating']
        print(rating1)
        with app.app_context():

            book_selected = db.session.execute(db.select(Books).where(Books.id == el)).scalar()
            print('uno',book_selected.rating)
            book_selected.rating = rating1
            db.session.commit()
            print(book_selected.rating)

    with app.app_context():
        # books = db.session.query(Books).all()

        book_selected = db.session.execute(db.select(Books).where(Books.id == el)).scalar()
        print(book_selected.title)
        return render_template('edit.html', book=book_selected)

@app.route("/delete/<il>")
def delete(il):
    with app.app_context():
        book_selected = db.session.execute(db.select(Books).where(Books.id == il)).scalar()
        db.session.delete(book_selected)
        db.session.commit()
    return redirect(url_for('home'))





#     result= db.session.execute(db.select(Books).order_by(Books.rating))
#     all_books = result.scalars()
#     print(all_books)


if __name__ == "__main__":

    app.run(debug=True)

