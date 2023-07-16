from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/categories', methods=['GET'])
def search_record():
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

    cursor.close()
    connection.close()

    return jsonify(record_list)

# #Api to search record by ID 
# @app.route('/categories/<int:record_id>',methods=['GET'])
# def search_record(record_id):
#     try :
#         connetion = db_connection
#         cursor = connection.cursor()


#         cursor.execute("SELECT * FROM categories WHERE id = %s",(record_id))
#         record = cursor.fetchone()
#         cursor.close()

#         if record : 


if __name__ == '__main__':
    app.run()


