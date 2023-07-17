from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000/categories"}})
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

#create new category
@app.route('/categories', methods=['POST'])
def create_category():
    connection = db_connection()
    cursor = connection.cursor()
    data = request.get_json()
    category_name = data['category_name']

    cursor.execute("INSERT INTO categories (category_name) VALUES (%s)", (category_name,))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'New category created'})

#delete category

@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    connection = db_connection()
    cursor = connection.cursor()

    # Check if the category exists
    cursor.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
    category = cursor.fetchone()

    if category is None:
        cursor.close()
        connection.close()
        return jsonify({'message': 'Category not found'})

    # Delete the category
    cursor.execute("DELETE FROM categories WHERE category_id = %s", (category_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Category deleted'})

#update the name of the category
@app.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    connection = db_connection()
    cursor = connection.cursor()

    # Check if the category exists
    cursor.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
    category = cursor.fetchone()

    if category is None:
        cursor.close()
        connection.close()
        return jsonify({'message': 'Category not found'})

    # Get the new category name from the request body
    data = request.get_json()
    new_category_name = data.get('category_name')

    # Update the category name
    cursor.execute("UPDATE categories SET category_name = %s WHERE category_id = %s", (new_category_name, category_id))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({'message': 'Category updated'})

if __name__ == '__main__':
    app.run()

