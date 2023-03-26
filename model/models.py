from portfolio.config import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, unique=False, nullable=True)
    lastname = db.Column(db.String, unique=False, nullable=True)
    email = db.Column(db.String, unique=False, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=False, nullable=True)
    author = db.Column(db.String, unique=False, nullable=True)
    isbn = db.Column(db.String, unique=True, nullable=True)
    status = db.Column(db.String, unique=False, nullable=True)


class UserHasBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bookid = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

