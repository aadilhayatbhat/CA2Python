from flask import Blueprint, jsonify, request
import mysql.connector

employees_bp = Blueprint('employees', __name__)

def db_connection():
    try:
        connection = mysql.connector.connect(
            host='34.245.104.62',
            user='library',
            password='password',
            database='library'
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

@employees_bp.route('/Employees', methods=['GET'])
def get_all_employees():
    connection = db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Employees")
            records = cursor.fetchall()

            record_list = []
            for record in records:
                record_dict = {'employee_id': record[0], 'name': record[1], 'position': record[2],'email': record[3],'phone': record[4]}
                record_list.append(record_dict)

            cursor.close()
            connection.close()

            return jsonify(record_list)
        except mysql.connector.Error as e:
            print(f"Error fetching data from the database: {e}")
            return jsonify({'message': 'An error occurred while fetching data'}), 500  # 500 Internal Server Error
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error

@employees_bp.route('/Employees/<int:record_id>', methods=['GET'])
def search_record_by_id(record_id):
    connection = db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Employees WHERE employee_id = %s", (record_id,))
            record = cursor.fetchone()

            connection.close()

            if record:
                record_dict = {'employee_id': record[0], 'name': record[1], 'position': record[2],'email': record[3],'phone': record[4]}
                return jsonify(record_dict), 200  # 200 OK - Successful request
            else:
                return jsonify({'message': 'Record not Found'}), 404  # 404 Not Found - Resource not found
        except mysql.connector.Error as e:
            print(f"Error fetching data from the database: {e}")
            return jsonify({'message': 'An error occurred while fetching data'}), 500  # 500 Internal Server Error
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error

@employees_bp.route('/Employees', methods=['POST'])
def add_employee():
    try:
        connection = db_connection()
        if not connection:
            return jsonify({'error': 'Database connection error'}), 500  # 500 Internal Server Error

        data = request.get_json()
        name = data.get('name')
        position = data.get('position')
        email = data.get('email')
        phone = data.get('phone')

        if not name or not email:
            return jsonify({'error': 'Invalid data. Both name and email are required.'}), 400  # 400 Bad Request

        cursor = connection.cursor()

        cursor.execute("INSERT INTO Employees (name, position, email, phone) VALUES (%s, %s, %s, %s)", (name, position, email, phone))

        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Employee added successfully'}), 201  # 201 Created
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # 500 Internal Server Error

@employees_bp.route('/Employees/<int:record_id>', methods=['DELETE'])
def delete_employee(record_id):
    connection = db_connection()
    if connection:
        try:
            connection.autocommit = True
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Employees WHERE employee_id = %s", (record_id,))
            record = cursor.fetchone()

            if not record:
                connection.close()
                return jsonify({'message': 'Record not Found'}), 404  # 404 Not Found - Resource not found

            cursor.execute("DELETE FROM Employees WHERE employee_id = %s", (record_id,))
            connection.commit()
            connection.close()

            return jsonify({'message': 'Employee deleted successfully'}), 200  # 200 OK - Successful request
        except mysql.connector.Error as e:
            print(f"Error deleting data from the database: {e}")
            return jsonify({'message': 'An error occurred while deleting data'}), 500  # 500 Internal Server Error
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error
