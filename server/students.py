from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def db_connection():
    connection = mysql.connector.connect(
        host='63.34.171.72',
        user='library',
        password='password',
        database='library'
    )
    return connection

@app.route('/students', methods=['GET'])
def get_all_students():
    connection = db_connection()
    if connection:
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
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error

@app.route('/students/<int:record_id>', methods=['GET'])
def search_record_by_id(record_id):
    connection = db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (record_id,))
        record = cursor.fetchone()

        connection.close()

        if record:
            record_dict = {'student_id': record[0], 'student_name': record[1], 'student_email': record[2]}
            return jsonify(record_dict), 200  # 200 OK - Successful request
        else:
            return jsonify({'message': 'Record not Found'}), 404  # 404 Not Found - Resource not found
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error


@app.route('/students/<string:student_name>', methods=['GET'])
def get_student_by_name(student_name):
    connection = db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students WHERE student_name = %s", (student_name,))
    record = cursor.fetchone()
    cursor.close()
    connection.close()

    if record:
        record_dict = {'student_id': record[0], 'student_name': record[1], 'student_email' :record[2]}
        return jsonify(record_dict)
    else:
        return jsonify({'message': 'student not found'})
if __name__ == '__main__':
    app.run()

