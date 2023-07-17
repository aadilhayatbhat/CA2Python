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

@app.route('/students', methods=['POST'])
def add_student():
    connection = db_connection()
    if not connection:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error

    data = request.get_json()
    student_name = data.get('student_name')
    student_email = data.get('student_email')

    if not student_name or not student_email:
        return jsonify({'message': 'Invalid data. Both student_name and student_email are required.'}), 400  # 400 Bad Request

    cursor = connection.cursor()
    cursor.execute("INSERT INTO students (student_name, student_email) VALUES (%s, %s)", (student_name, student_email,))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({'message': 'Student added successfully'}), 201  # 201 Created

#update student 

@app.route('/students/<int:record_id>', methods=['PUT'])
def update_student(record_id):
    connection = db_connection()
    if not connection:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error

    connection.autocommit = True
    cursor = connection.cursor()

    # Check if the student record exists
    cursor.execute("SELECT * FROM students WHERE student_id = %s", (record_id,))
    record = cursor.fetchone()

    if not record:
        connection.close()
        return jsonify({'message': 'Record not Found'}), 404  # 404 Not Found - Resource not found

    # Get the updated data from the request
    data = request.get_json()
    student_name = data.get('student_name')
    student_email = data.get('student_email')

    if not student_name or not student_email:
        connection.close()
        return jsonify({'message': 'Invalid data. Both student_name and student_email are required.'}), 400  # 400 Bad Request

    # Update the student record
    cursor.execute("UPDATE students SET student_name = %s, student_email = %s WHERE student_id = %s",
                   (student_name, student_email, record_id))
    connection.commit()
    connection.close()

    return jsonify({'message': 'Record updated successfully'}), 200  # 200 OK - Successful request



if __name__ == '__main__':
    app.run()
