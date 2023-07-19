from flask import Flask
from flask_cors import CORS
from server.BookReviews import book_reviews_bp
from server.borrowed_books import borrowed_books_bp
from server.categories import categories_bp
from server.Employees import employees_bp
from server.kitaab import books_bp
from server.students import students_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(book_reviews_bp)
app.register_blueprint(borrowed_books_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(books_bp)
app.register_blueprint(students_bp)

if __name__ == '__main__':
    app.run()
