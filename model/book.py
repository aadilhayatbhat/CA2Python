class BookReview:
    def __init__(self, review_id, book_id, student_id, review_date, comments):
        self.review_id = review_id
        self.book_id = book_id
        self.student_id = student_id
        self.review_date = review_date
        self.comments = comments

    def to_dict(self):
        return {
            'review_id': self.review_id,
            'book_id': self.book_id,
            'student_id': self.student_id,
            'review_date': self.review_date,
            'comments': self.comments
        }
