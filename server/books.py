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
def get_all_students():
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
    
if __name__ == '__main__':
    app.run()