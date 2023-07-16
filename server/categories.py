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

@app.route('/categories', methods=['GET'])
def get_all_categories():
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM categories")
    records = cursor.fetchall()

    record_list = []
    for record in records:
        record_dict = {'category_id': record[0], 'category_name': record[1]}
        record_list.append(record_dict)

    cursor.close()
    connection.close()

    return jsonify(record_list)

@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    connection = db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
    record = cursor.fetchone()
    cursor.close()
    connection.close()

    if record:
        record_dict = {'category_id': record[0], 'category_name': record[1]}
        return jsonify(record_dict)
    else:
        return jsonify({'message': 'Category not found'})

@app.route('/categories/<string:category_name>', methods=['GET'])
def get_category_by_name(category_name):
    connection = db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM categories WHERE category_name = %s", (category_name,))
    record = cursor.fetchone()
    cursor.close()
    connection.close()

    if record:
        record_dict = {'category_id': record[0], 'category_name': record[1]}
        return jsonify(record_dict)
    else:
        return jsonify({'message': 'Category not found'})

if __name__ == '__main__':
    app.run()