from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def db_connection():
    try:
        connection = mysql.connector.connect(
            host='63.34.171.72',
            user='library',
            password='password',
            database='library'
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}")
        return None
    


@app.route('/books', methods=['GET'])
def get_all_books():
    connection = db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM books")
            records = cursor.fetchall()

            record_list = []
            for record in records:
                record_dict = {'book_id': record[0], 'title': record[1], 'author': record[2], 'category_id': record[3], 'available_books': record[4]}
                record_list.append(record_dict)

            cursor.close()
            connection.close()

            return jsonify(record_list)
        except mysql.connector.Error as e:
            print(f"Error fetching data from the database: {e}")
            return jsonify({'message': 'An error occurred while fetching data'}), 500  # 500 Internal Server Error
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error

 #create api for books   

@app.route('/books/<int:record_id>', methods=['GET'])
def search_record_by_id(record_id):
    connection = db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM books WHERE book_id = %s", (record_id,))
            record = cursor.fetchone()

            connection.close()

            if record:
                record_dict = {'book_id': record[0], 'title': record[1], 'author': record[2], 'category_id': record[3], 'available_books': record[4]}
                return jsonify(record_dict), 200  # 200 OK - Successful request
            else:
                return jsonify({'message': 'Record not Found'}), 404  # 404 Not Found - Resource not found
        except mysql.connector.Error as e:
            print(f"Error fetching data from the database: {e}")
            return jsonify({'message': 'An error occurred while fetching data'}), 500  # 500 Internal Server Error
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error
    

def check_category_id_exist(category_id):
    connection = db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
            record = cursor.fetchone()
            cursor.close()
            connection.close()
            return True if record else False
        except mysql.connector.Error as e:
            print(f"Error checking category_id in the database: {e}")
            return False
    else:
        return False



@app.route('/books', methods=['POST'])
def add_book():
    connection = db_connection()
    if not connection:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error

    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    category_id = data.get('category_id')
    available_books = data.get('available_books')

# Check if category_id exist in the database
    if not check_category_id_exist(category_id):
            return jsonify({'message': 'Invalid category_id'}), 400  # 400 Bad Request

    if not title or not author or not category_id or available_books is None:
        return jsonify({'message': 'Invalid data. All fields (title, author, category_id, available_books) are required.'}), 400  # 400 Bad Request

    cursor = connection.cursor()
    cursor.execute("INSERT INTO books (title, author, category_id, available_books) VALUES (%s, %s, %s, %s)", (title, author, category_id, available_books,))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({'message': 'Book added successfully'}), 201  # 201 Created

#delete

@app.route('/books/<int:record_id>', methods=['DELETE'])
def delete_book(record_id):
    connection = db_connection()

    if not connection:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error

    cursor = connection.cursor()

    try:
        # Check if the book exists before attempting to delete it
        cursor.execute("SELECT * FROM books WHERE book_id = %s", (record_id,))
        book = cursor.fetchone()
        if not book:
            return jsonify({'message': 'Book not found'}), 404  # 404 Not Found - Resource not found

        # Delete book reviews first (Assuming there's a foreign key constraint)
        cursor.execute("DELETE FROM BookReviews WHERE book_id = %s", (record_id,))

        # Now delete the book record
        cursor.execute("DELETE FROM books WHERE book_id = %s", (record_id,))
        connection.commit()

        return jsonify({'message': 'Book deleted successfully'}), 200  # 200 OK
    except mysql.connector.Error as e:
        print(f"Error deleting the book: {e}")
        return jsonify({'message': 'An error occurred while deleting the book'}), 500  # 500 Internal Server Error
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run()