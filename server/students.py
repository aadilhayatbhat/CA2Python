from flask import Flask, jsonify
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

@app.route('/students', methods=['GET'])
def get_all_students():
    connection = db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM students")
            records = cursor.fetchall()

            record_list = []
            for record in records:
                record_dict = {'student_id': record[0], 'student_name': record[1], 'student_email': record[2]}
                record_list.append(record_dict)

            cursor.close()
            connection.close()

            return jsonify(record_list)
        except mysql.connector.Error as e:
            print(f"Error fetching data from the database: {e}")
            return jsonify({'message': 'An error occurred while fetching data'}), 500  # 500 Internal Server Error
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error

@app.route('/students/<int:record_id>', methods=['GET'])
def search_record_by_id(record_id):
    connection = db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = %s", (record_id,))
            record = cursor.fetchone()

            connection.close()

            if record:
                record_dict = {'student_id': record[0], 'student_name': record[1], 'student_email': record[2]}
                return jsonify(record_dict), 200  # 200 OK - Successful request
            else:
                return jsonify({'message': 'Record not Found'}), 404  # 404 Not Found - Resource not found
        except mysql.connector.Error as e:
            print(f"Error fetching data from the database: {e}")
            return jsonify({'message': 'An error occurred while fetching data'}), 500  # 500 Internal Server Error
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error

@app.route('/students/<int:record_id>', methods=['DELETE'])
def delete_student(record_id):
    connection = db_connection()
    if connection:
        try:
            connection.autocommit = True
            cursor = connection.cursor()

            # Check if the student record exists
            cursor.execute("SELECT * FROM students WHERE student_id = %s", (record_id,))
            record = cursor.fetchone()

            if not record:
                connection.close()
                return jsonify({'message': 'Record not Found'}), 404  # 404 Not Found - Resource not found

            # Delete the student record
            cursor.execute("DELETE FROM students WHERE student_id = %s", (record_id,))
            connection.commit()
            connection.close()

            return jsonify({'message': 'Record deleted successfully'}), 200  # 200 OK - Successful request
        except mysql.connector.Error as e:
            print(f"Error deleting data from the database: {e}")
            return jsonify({'message': 'An error occurred while deleting data'}), 500  # 500 Internal Server Error
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error

if __name__ == '__main__':
    app.run()