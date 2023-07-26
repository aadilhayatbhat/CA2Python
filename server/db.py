import mysql.connector

db_connection = mysql.connector.connect(
    host = '34.245.104.62',
    user = 'library',
    password = 'password',
    database = 'library'

)

# connection = db_connection