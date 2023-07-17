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
    

@app.route('/bookreview', methods=['GET'])
def get_all_book_reviews():
    connection = db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM BookReviews")
        records = cursor.fetchall()

        record_list = []
        for record in records:
            record_dict = {'review_id': record[0], 'book_id': record[1], 'student_id': record[2], 'review_date': record[3], 'rating': record[4],'comments': record[5]}
            record_list.append(record_dict)

        cursor.close()
        connection.close()

        return jsonify(record_list)
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error


if __name__ == '__main__':
    app.run()