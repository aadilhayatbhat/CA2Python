from flask import Blueprint, jsonify, request
from book_service import BookService

book_blueprint = Blueprint('book_blueprint', __name__)
book_service = BookService()

@book_blueprint.route('', methods=['GET'])
def get_all_book_reviews():
    record_list = book_service.get_all_book_reviews()
    if record_list is not None:
        return jsonify(record_list)
    else:
        return jsonify({'message': 'Database connection error'}), 500  # 500 Internal Server Error

@book_blueprint.route('', methods=['POST'])
def create_book_review():
    data = request.get_json()
    review_id = data.get('review_id')
    book_id = data.get('book_id')
    comments = data.get('comments')
    student_id = data.get('student_id')
    response = book_service.create_book_review(review_id, student_id, book_id, comments)
    return jsonify(response)
