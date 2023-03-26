from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
key = b'if54OYWdN410-ixPfNxAJ12oIw8tZDnRUF3vCDy7shA='
dbname = "sqlite:///books.db"
# Zeile 4 musste ich den Absoluten Pfad meiner DB angeben ansonsten hat das Programm die DB nicht importiert und erkannt