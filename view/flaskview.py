from flask import Flask, session, render_template, redirect, request, url_for
from portfolio.config import db, dbname
from portfolio.controller.controllers import Usercontroller, Bookcontroller
# create the app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = dbname
db.init_app(app)
app.secret_key = "lkjkljasdfklaskjf"
#TODO

@app.route("/")
def show_homepage():
    '''
    Shows the start page
    :return:
    '''
    session.clear()
    return render_template("homepage.html")


@app.route("/login", methods=['POST'])
def login():
    """Used when the user filled out the login form and redirects the user to home.html
    in case, that the user has been successfully logged in. Otherwise, he is redirected to the homepage.html"""
    session.clear()

    email = request.form.get("email")
    password = request.form.get("password")

    user_login = Usercontroller().login(email, password)

    if user_login is not None:
        session["userid"] = user_login.id
        return redirect(url_for("showHome"))

    else:
        return redirect(url_for("show_homepage"))



@app.route("/logoutuser")
def logoutUser():
    session.clear()
    return render_template("homepage.html")


@app.route("/createUser", methods=['POST'])
def create_user():
    '''Used, after the user has filled out the registration form and submits.
    User is now created and the user is redirected to the homepage.html'''

    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    password = request.form.get("password")
    user_mail = request.form.get("user_mail")

    Usercontroller().create_user(firstname, lastname, user_mail, password)

    return redirect(url_for("show_homepage"))


@app.route("/borrowbook", methods=['POST'])
def borrow_book():
    '''Used, when the user clicks reserve in the frontend. Afterwards, the user is redirected to /showhome'''
    bookid = request.form["book-button"]
    userid = session["userid"]

    borrow_book = Bookcontroller().reserve_book(int(userid), int(bookid))

    if borrow_book:
        return redirect(url_for("showHome"))


@app.route("/showhome")
def showHome():
    """Shows the book overview (home.html) with available and reserved books"""
    books = Bookcontroller().get_all_books()
    not_reserved_books = []
    for book in books:
        if book.status == "verfügbar":
            not_reserved_books.append(book)

    try:
        if session.get("userid"):
            borrowed_books = Bookcontroller().get_all_books_for_user(session["userid"])
            return render_template("home.html", not_reserved_books=not_reserved_books, borrowed_books=borrowed_books)

        else:
            print("session not set!")
            return redirect(url_for("show_homepage"))
    except:
        return redirect(url_for("show_homepage"))



@app.route("/showCreateUser")
def show_create_user():
    """Opens the createuser.html"""
    return render_template("createuser.html")


@app.route("/logout")
def logout():
    # THIS FUNCTION IS OBSOLETE. YOU DON'T HAVE TO USE THIS IN YOUR PORTFOLIO
    session.clear()


with app.app_context():
    db.create_all()
app.run(debug=True)
