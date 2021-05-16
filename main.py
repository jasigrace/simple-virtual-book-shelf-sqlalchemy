from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
#Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()


@app.route('/')
def home():
    ##READ ALL RECORDS
    all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # CREATE RECORD
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # UPDATE RECORD
        book_id = request.form["id"]
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template("edit_rating.html", book=book_selected)


@app.route("/delete")
def delete():
    book_id = request.args.get('id')

    # DELETE A RECORD BY ID
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)


# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection1.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
#

# class BookShelf(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     title = db.Column(db.String(250), unique=True, nullable=False)
#     author = db.Column(db.String(250), nullable=False)
#     rating = db.Column(db.Float, nullable=False)
#
#     def __repr__(self):
#         return f'<BookShelf {self.title}>'


# db.create_all()
#
#
# new_book = BookShelf(id=2, title="Twighlighy", author="J. K. Rowling", rating=9.3)
# db.session.add(new_book)
# db.session.commit()

# Read all books in book shelf
# all_books = db.session.query(BookShelf).all()
# print(all_books)

# Read a particular record by query
# book = BookShelf.query.filter_by(title="Twighlighy").first()
# print(book)

# Update a particular record by query
# book_to_update = BookShelf.query.filter_by(title="Twighlighy").first()
# book_to_update.title = "Twighlight"
# db.session.commit()

# all_books = db.session.query(BookShelf).all()
# print(all_books)


# Update a record by PRIMARY KEY
# book_id = 2
# book_to_update = BookShelf.query.get(book_id)
# book_to_update.title = "Twighlight 2"
# db.session.commit()

# Delete a particular record by primary key

# book_id = 2
# book_to_delete = BookShelf.query.get(book_id)
# db.session.delete(book_to_delete)
# db.session.commit()
