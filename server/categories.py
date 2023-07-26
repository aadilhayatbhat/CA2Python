from flask import Blueprint, request, jsonify
import mysql.connector

categories_bp = Blueprint('categories', __name__)

def db_connection():
    connection = mysql.connector.connect(
        host='40.85.131.117',
        user='library',
        password='password',
        database='library'
    )
    return connection

@categories_bp.route('/categories', methods=['GET'])
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

@categories_bp.route('/categories/<int:category_id>', methods=['GET'])
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

@categories_bp.route('/categories', methods=['POST'])
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

@categories_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    connection = db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
    category = cursor.fetchone()

    if category is None:
        cursor.close()
        connection.close()
        return jsonify({'message': 'Category not found'})

    cursor.execute("DELETE FROM categories WHERE category_id = %s", (category_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Category deleted'})

@categories_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    connection = db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
    category = cursor.fetchone()

    if category is None:
        cursor.close()
        connection.close()
        return jsonify({'message': 'Category not found'})

    data = request.get_json()
    new_category_name = data.get('category_name')

    cursor.execute("UPDATE categories SET category_name = %s WHERE category_id = %s", (new_category_name, category_id))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({'message': 'Category updated'})
