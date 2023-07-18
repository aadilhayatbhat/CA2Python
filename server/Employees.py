from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000/Employees"}})
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
    
@app.route('/Employees', methods=['GET'])
def get_all_students():
    connection = db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Employees")
            records = cursor.fetchall()

            record_list = []
            for record in records:
                record_dict = {'employee_id': record[0], 'name': record[1], 'position': record[2],'email': record[3],'phone': record[4],}
                record_list.append(record_dict)

            cursor.close()
            connection.close()

            return jsonify(record_list)
        except mysql.connector.Error as e:
            print(f"Error fetching data from the database: {e}")
            return jsonify({'message': 'An error occurred while fetching data'}), 500  # 500 Internal Server Error
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error


if __name__ == '__main__':
    app.run()
