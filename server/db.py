import mysql.connector

db_connection = mysql.connector.connect(
    host = '40.85.131.117',
    user = 'library',
    password = 'password',
    database = 'library'

)

# connection = db_connection