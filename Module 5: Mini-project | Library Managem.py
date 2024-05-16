import mysql.connector
from mysql.connector import Error
from datetime import datetime

db_name = "library_management"
user = "root" 
host = "127.0.0.1"
port = "3306"

class Database:
    def __init__(self, db_name, user, host, port):
        self.db_name = db_name
        self.user = user
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                database=self.db_name,
                user=self.user,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor()
            print("Connected to MySQL Database")
        except Error as e:
            print(f"Error: {e}")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
        except Error as e:
            print(f"Error: {e}")

    def fetch_all(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchall()  
            return result
        except Error as e:
            print(f"Error: {e}")

    def close(self):
        if self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("MySQL Connection Closed")

class Book:
    def __init__(self, title, author, isbn, genre, publication_date, availability=True):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.publication_date = publication_date
        self.availability = availability

    def save_to_db(self, db):
        query = "SELECT id FROM books WHERE isbn = %s"
        result = db.fetch_all(query, (self.isbn,))
        if result:
            print(f"Book with ISBN {self.isbn} already exists in the database.")
        else:
            query = """
            INSERT INTO books (title, author, isbn, genre, publication_date, availability)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            db.execute_query(query, (self.title, self.author, self.isbn, self.genre, self.publication_date, self.availability))
            print(f"Book '{self.title}' added to the database.")

if __name__ == "__main__":
    db = Database(db_name, user, host, port)
    db.connect()


    books_to_add = [
        Book("Python. Crash course", "Eric Matthes", "9781593279288", "Education", "2015-07-11"),
        Book("1984", "George Orwell", "9780451524935", "Fiction", "1949-06-08"),
        Book("Pride and Prejudice", "Jane Austen", "9780141439518", "Romance", "1813-01-28"),
        Book("The Catcher in the Rye", "J.D. Salinger", "9780316769488", "Fiction", "1951-07-16"),
        Book("The Hobbit", "J.R.R. Tolkien", "9780547928227", "Fantasy", "1937-09-21")
    ]

    for book in books_to_add:
        book.save_to_db(db)


    query = "SELECT * FROM books;"
    db.cursor.execute(query)
    for row in db.cursor.fetchall():
        print(row)

    db.close()