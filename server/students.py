from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/students', methods=['GET'])
def search_record():
    connection = mysql.connector.connect(
        host='63.34.171.72',
        user='library',
        password='password',
        database='library'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    record_list = []
    for record in records:
        record_dict = {'student_id': record[0], 'student_name': record[1], 'student_mail': record[2]}
        record_list.append(record_dict)

    cursor.close()
    connection.close()

    return jsonify(record_list)

if __name__ == '__main__':
    app.run()

