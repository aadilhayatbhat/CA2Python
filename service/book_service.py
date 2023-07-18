from db_connection import db_connection
from model.book import BookReview

class BookService:
    def get_all_book_reviews(self):
        connection = db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM BookReviews")
            records = cursor.fetchall()
            record_list = []
            for record in records:
                review = BookReview(record[0], record[1], record[2], record[3], record[4])
                record_list.append(review.to_dict())
            cursor.close()
            connection.close()
            return record_list
        else:
            return None

    def create_book_review(self, review_id, student_id, book_id, comments):
        connection = db_connection()
        if connection is None:
            return {'message': 'Database connection error'}, 500  # 500 Internal Server Error
        cursor = connection.cursor()
        insert_query = "INSERT INTO BookReviews (review_id, student_id, book_id, comments) VALUES (%s, %s, %s, %s)"
        values = (review_id, student_id, book_id, comments)
        try:
            cursor.execute(insert_query, values)
            connection.commit()
            cursor.close()
            connection.close()
            return {'message': 'Book review created successfully'}
        except mysql.connector.Error as e:
            return {'message': f'Database error while creating the book review: {e}'}, 500  # 500 Internal Server Error
