import mysql.connector

db_connection = mysql.connector.connect(
    host = '63.34.171.72',
    user = 'library',
    password = 'password',
    database = 'library'

)

# connection = db_connection