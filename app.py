from flask import Flask
from flask_cors import CORS
from routes.book_routes import book_blueprint
from db_connection import db_connection

app = Flask(__name__)
CORS(app)

app.config['DB_CONNECTION'] = db_connection

app.register_blueprint(book_blueprint, url_prefix='/bookreview')

if __name__ == '__main__':
    app.run()
