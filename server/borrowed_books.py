from flask import Blueprint, jsonify, request
import mysql.connector

borrowed_books_bp = Blueprint('borrowed_books', __name__)

def db_connection():
    try:
        connection = mysql.connector.connect(
            host='40.85.131.117',
            user='library',
            password='password',
            database='library'
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

@borrowed_books_bp.route('/borrowed_books', methods=['GET'])
def get_all_borrowed_books():
    connection = db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM borrowed_books")
            records = cursor.fetchall()

            record_list = []
            for record in records:
                record_dict = {'transaction_id': record[0], 'student_id': record[1], 'book_id': record[2], 'borrow_date': record[3], 'due_date': record[4], }
                record_list.append(record_dict)

            cursor.close()
            connection.close()

            return jsonify(record_list)
        except mysql.connector.Error as e:
            print(f"Error fetching data from the database: {e}")
            return jsonify({'message': 'An error occurred while fetching data'}), 500  # 500 Internal Server Error
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error

@borrowed_books_bp.route('/borrowed_books/<int:record_id>', methods=['GET'])
def search_record_by_id(record_id):
    connection = db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM borrowed_books WHERE transaction_id = %s", (record_id,))
            record = cursor.fetchone()

            connection.close()

            if record:
                record_dict = {'transaction_id': record[0], 'student_id': record[1], 'book_id': record[2], 'borrow_date': record[3], 'due_date': record[4], }
                return jsonify(record_dict), 200  # 200 OK - Successful request
            else:
                return jsonify({'message': 'Record not Found'}), 404  # 404 Not Found - Resource not found
        except mysql.connector.Error as e:
            print(f"Error fetching data from the database: {e}")
            return jsonify({'message': 'An error occurred while fetching data'}), 500  # 500 Internal Server Error
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error

def check_student_id_exist(student_id):
    connection = db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
            record = cursor.fetchone()
            cursor.close()
            connection.close()
            return True if record else False
        except mysql.connector.Error as e:
            print(f"Error checking student_id in the database: {e}")
            return False
    else:
        return False

def check_book_id_exist(book_id):
    connection = db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
            record = cursor.fetchone()
            cursor.close()
            connection.close()
            return True if record else False
        except mysql.connector.Error as e:
            print(f"Error checking book_id in the database: {e}")
            return False
    else:
        return False

@borrowed_books_bp.route('/borrowed_books', methods=['POST'])
def create_borrowed_book():
    connection = db_connection()
    if connection:
        try:
            data = request.get_json()
            student_id = data.get('student_id')
            book_id = data.get('book_id')
            borrow_date = data.get('borrow_date')
            due_date = data.get('due_date', None)  # Use None as the default value

            # Check if student_id and book_id exist in the database
            if not check_student_id_exist(student_id):
                return jsonify({'message': 'Invalid student_id'}), 400  # 400 Bad Request
            if not check_book_id_exist(book_id):
                return jsonify({'message': 'Invalid book_id'}), 400  # 400 Bad Request

            cursor = connection.cursor()
            insert_query = "INSERT INTO borrowed_books (student_id, book_id, borrow_date, due_date) VALUES (%s, %s, %s, %s)"
            values = (student_id, book_id, borrow_date, due_date)
            cursor.execute(insert_query, values)
            connection.commit()
            cursor.close()
            connection.close()

            return jsonify({'message': 'Borrowed book created successfully'}), 201  # 201 Created - Resource created
        except mysql.connector.Error as e:
            print(f"Error inserting data into the database: {e}")
            return jsonify({'message': 'An error occurred while creating borrowed book'}), 500  # 500 Internal Server Error
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error

@borrowed_books_bp.route('/borrowed_books/<int:record_id>', methods=['PUT'])
def update_borrowed_book(record_id):
    connection = db_connection()
    if connection:
        try:
            data = request.get_json()
            student_id = data.get('student_id')
            book_id = data.get('book_id')
            borrow_date = data.get('borrow_date')
            due_date = data.get('due_date', None)  # Use None as the default value

            # Check if the record exists in the database
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM borrowed_books WHERE transaction_id = %s", (record_id,))
            record = cursor.fetchone()

            if not record:
                cursor.close()
                connection.close()
                return jsonify({'message': 'Record not found'}), 404  # 404 Not Found - Resource not found

            # Check if the updated student_id and book_id exist in their respective tables
            if student_id is not None and not check_student_id_exist(student_id):
                return jsonify({'message': 'Invalid student_id'}), 400  # 400 Bad Request
            if book_id is not None and not check_book_id_exist(book_id):
                return jsonify({'message': 'Invalid book_id'}), 400  # 400 Bad Request

            # Update the borrowed book record
            update_query = "UPDATE borrowed_books SET "
            updates = []
            values = []

            if student_id is not None:
                updates.append("student_id = %s")
                values.append(student_id)
            if book_id is not None:
                updates.append("book_id = %s")
                values.append(book_id)
            if borrow_date is not None:
                updates.append("borrow_date = %s")
                values.append(borrow_date)
            if due_date is not None:
                updates.append("due_date = %s")
                values.append(due_date)

            update_query += ", ".join(updates)
            update_query += " WHERE transaction_id = %s"
            values.append(record_id)

            cursor.execute(update_query, tuple(values))
            connection.commit()
            cursor.close()
            connection.close()

            return jsonify({'message': 'Borrowed book record updated successfully'}), 200  # 200 OK - Successful request
        except mysql.connector.Error as e:
            print(f"Error updating data in the database: {e}")
            return jsonify({'message': 'An error occurred while updating borrowed book record'}), 500  # 500 Internal Server Error
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error
    



@borrowed_books_bp.route('/borrowed_books/<int:record_id>', methods=['DELETE'])
def delete_borrowed_book(record_id):
    connection = db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Check if the record exists in the database
            cursor.execute("SELECT * FROM borrowed_books WHERE transaction_id = %s", (record_id,))
            record = cursor.fetchone()

            if not record:
                cursor.close()
                connection.close()
                return jsonify({'message': 'Record not found'}), 404  # 404 Not Found - Resource not found

            # Delete the borrowed book record
            delete_query = "DELETE FROM borrowed_books WHERE transaction_id = %s"
            cursor.execute(delete_query, (record_id,))
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({'message': 'Borrowed book record deleted successfully'}), 200  # 200 OK - Successful request
        except mysql.connector.Error as e:
            print(f"Error deleting data from the database: {e}")
            return jsonify({'message': 'An error occurred while deleting borrowed book record'}), 500  # 500 Internal Server Error
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error


