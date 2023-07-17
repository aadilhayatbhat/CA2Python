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

@app.route('/borrowed_books', methods=['GET'])
def get_all_borrowed_books():
    connection = db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM borrowed_books")
            records = cursor.fetchall()

            record_list = []
            for record in records:
                record_dict = {'transaction_id': record[0], 'student_id': record[1], 'book_id': record[2], 'borrow_date': record[3], 'due_date': record[4], 'returned_date': record[5]}
                record_list.append(record_dict)

            cursor.close()
            connection.close()

            return jsonify(record_list)
        except mysql.connector.Error as e:
            print(f"Error fetching data from the database: {e}")
            return jsonify({'message': 'An error occurred while fetching data'}), 500  # 500 Internal Server Error
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error


@app.route('/borrowed_books/<int:record_id>', methods=['GET'])
def search_record_by_id(record_id):
    connection = db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM borrowed_books WHERE book_id = %s", (record_id,))
            record = cursor.fetchone()

            connection.close()

            if record:
                record_dict = {'transaction_id': record[0], 'student_id': record[1], 'book_id': record[2], 'borrow_date': record[3], 'due_date': record[4], 'returned_date': record[5]}
                return jsonify(record_dict), 200  # 200 OK - Successful request
            else:
                return jsonify({'message': 'Record not Found'}), 404  # 404 Not Found - Resource not found
        except mysql.connector.Error as e:
            print(f"Error fetching data from the database: {e}")
            return jsonify({'message': 'An error occurred while fetching data'}), 500  # 500 Internal Server Error
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error

if __name__ == '__main__':
    app.run()