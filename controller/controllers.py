from portfolio.model.models import User, Book, UserHasBook
from cryptography.fernet import Fernet
from portfolio.config import key, db
import logging

logging.basicConfig(filename="logging.log", encoding="utf-8", level=logging.INFO, format="%(levelname)s: %(asctime)s %(message)s")

class Usercontroller:

    def __init__(self):
         self.dbc = Databasecontroller()

    def login(self, email, pw):
        '''
        Loggs a user in with given email and passwort
        :param email: Emailaddress of the user
        :param pw: Password of the user
        :return: User object if users exists in DB, None otherwise
        '''
        try:
            login_user = self.dbc.find_user_by_credentials(email, pw)

            if login_user:
                logging.info("user was logged in!")
                return login_user

            if login_user is None:
                logging.warning("user logging failed!")
                return None
        except:
            logging.error("user logging failed!")
            return print("failed to login user")

    def create_user(self, firstname, lastname, user_mail, password):
        '''
        Creates a new User in Database.
        :param firstname:
        :param lastname:
        :param email:
        :param password:
        :return: Returns True if creation has been successfully. False otherwise
        '''
        try:
            f = Fernet(key)
            # convert password to bytes
            password = bytes(password,"utf-8")
            password = f.encrypt(password)
            password = password.decode("utf-8")

            create_user = User(firstname=firstname, lastname=lastname, email=user_mail, password=password)

            created_user = self.dbc.create_user(create_user)

            if created_user:
                logging.info("user was created!")
                return True

            else:
                logging.warning("user creation failed!")
                return None
        except:
            logging.error("user register failed!")
            return print("failed to register user")


class Databasecontroller:

    def find_user_by_credentials(self, email, pw):
        '''
        Searches a User by the credentials in DB
        :param email:
        :param pw:
        :return: User object if the user can be found, None otherwise
        '''
        try:
            f = Fernet(key)

            users = User.query.filter_by(email=email).all()

            for user in users:
                decrypted_pw = f.decrypt(user.password).decode('utf-8')

                if decrypted_pw == pw:
                    logging.info("user was found!")
                    return user

                else:
                    return None
        except:
            logging.error("user finding failed!")
            return print("failed to find user")

    def add_reservation(self,reservation):
        '''
        Adds a reservation for a book in the DB
        :param reservation:
        '''
        try:
            db.session.add(reservation)
            db.session.commit()
            logging.info("reservation was added to the database!")
            return True
        except:
            logging.error("book reservation failed!")
            return print("can not reserve book")

    def create_user(self, user):
        '''
        Creates a user in Databse
        :param user:
        '''
        try:
            db.session.add(user)
            db.session.commit()
            logging.info("user was added to the database!")
            return True
        except:
            logging.error("user creation in database failed!")
            return print("can not create user")

    def get_all_books(self):
        '''
        Gets a list of all book in the Database
        :return: List of Books
        '''
        try:
            books = Book.query.all()
            return books
        except:
            logging.error("finding books in database failed!")
            return print("failed to get all books")

    def change_reservestatus(self,bookid,status):
        '''
        Sets the revervation of a book
        :param bookid: The id of the book
        :param status: The status the book with the given ID should have
        '''
        try:
            book = self.get_book_by_id(bookid)
            book.status = status
            logging.info("Book status was changed!")
            db.session.commit()
            return book
        except:
            logging.error("change book status in database failed!")
            return print("change reserve status failed!")

    def get_reserved_books_for_user(self,userid):
        '''
        Fetches all books from the Database a user has reserved
        :param userid:
        :return: A list of books
        '''
        try:
            user_books_list_id = []
            borrowed_books = []
            user_books = UserHasBook.query.filter_by(userid=userid).all()

            for user_book in user_books:
                user_books_list_id.append(user_book.bookid)

            for user_book_id in user_books_list_id:
                borrowed_book = self.get_book_by_id(user_book_id)
                borrowed_books.append(borrowed_book)

            return borrowed_books

        except:
            logging.error("get reserved books failed!")
            return print("reserved books for user are unavailable!")

    def get_book_by_id(self,bookid):
        '''
        Finds a book by its ID
        :param bookid:
        :return: A book object if the id can be found, None otherwise
        '''
        try:
            book = Book.query.filter_by(id=bookid).first()
            return book

        except:
            logging.error("finding books by id failed!")
            return print("can´t find book by it´s id")

class Bookcontroller():
    def __init__(self):
        self.dbc = Databasecontroller()

    def get_all_books(self):
        '''
        Returns all books
        :return: a list of books or None
        '''
        books = self.dbc.get_all_books()
        return books

    def reserve_book(self,userid,bookid):
        '''
        Reserves a book with the given id for the given user id
        :param userid:
        :param bookid:
        '''
        # Hint: check if book isn't already reserved (e.g. page reload)

        try:
            reservation = UserHasBook(userid=userid, bookid=bookid)

            if self.dbc.add_reservation(reservation):
                self.dbc.change_reservestatus(bookid, "reserviert")
                return True
        except:
            logging.error("book reservation failed!")
            return print("can´t reserve book")

    def get_all_books_for_user(self,user_id):
        '''
        Returns all books reserved by a user
        :param user_id:
        :return:
        '''
        try:
            user_books = self.dbc.get_reserved_books_for_user(user_id)
            return user_books
        except:
            logging.error("getting books for user failed!")
            return print("failed getting books of user")




