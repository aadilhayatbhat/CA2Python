from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/categories', methods=['GET'])
def search_record():
    try:
        connection = mysql.connector.connect(
            host='63.34.171.72',
            user='library',
            password='password',
            database='library'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM categories")
        records = cursor.fetchall()

        record_list = []
        for record in records:
            record_dict = {'category_id': record[0], 'category_name': record[1]}
            record_list.append(record_dict)

        return jsonify(record_list)

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)})

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run()
