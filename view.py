# This file contains routes related to books, reviews, and comments in the application.
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Book, Review, Comment, User
from extensions import db

book_bp = Blueprint('api', __name__)

# get all books 
@book_bp.route('/bookList', methods=['GET'])
def get_all_books():
    books = Book.query.all()

    books_list = []
    for book in books:
        reviews = Review.query.filter_by(book_id=book.id).all()

        book_details = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "genre": book.genre,
            "publication_year": book.publication_year,
            "reviews": [
                {
                    "id": review.id,
                    "rating": review.rating,
                    "text": review.text,
                    "created_at": review.created_at,
                    "comments": [
                        {
                            "id": comment.id,
                            "text": comment.text,
                            "created_at": comment.created_at,
                        }
                        for comment in Comment.query.filter_by(review_id=review.id).all()
                    ],
                }
                for review in reviews
            ],
        }

        books_list.append(book_details)

    return jsonify({"books": books_list}), 200

# add book
@book_bp.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    genre = data.get('genre')
    publication_year = data.get('publication_year')

    new_book = Book(title=title, author=author, genre=genre, publication_year=publication_year)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({"message": "Book added successfully"}), 201

# add review
@book_bp.route('/books/<int:book_id>/reviews', methods=['POST'])
@jwt_required()
def add_review(book_id):
    data = request.get_json()
    rating = data.get('rating')
    text = data.get('text')

    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    book = Book.query.get_or_404(book_id)

    new_review = Review(rating=rating, text=text, user=current_user, book=book)
    db.session.add(new_review)
    db.session.commit()

    return jsonify({"message": "Review added successfully"}), 201


# add comment 
@book_bp.route('/reviews/<int:review_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(review_id):
    data = request.get_json()
    text = data.get('text')

    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    review = Review.query.get_or_404(review_id)

    new_comment = Comment(text=text, user=current_user, review=review)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({"message": "Comment added successfully"}), 201




# user can edit delete there commentes and reviews 

@book_bp.route('/reviews/<int:review_id>/edit', methods=['PUT'])
@jwt_required()
def edit_review(review_id):
    data = request.get_json()
    new_text = data.get('text')

    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    review = Review.query.get_or_404(review_id)

    if review.user != current_user:
        return jsonify({"error": "You are not authorized to edit this review"}), 403

    review.text = new_text
    db.session.commit()

    return jsonify({"message": "Review edited successfully"}), 200


# Delete review
@book_bp.route('/reviews/<int:review_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    review = Review.query.get_or_404(review_id)

    if review.user != current_user:
        return jsonify({"error": "You are not authorized to delete this review"}), 403
    
    Comment.query.filter_by(review_id=review_id).delete()#also ythe comment will be delete 

    db.session.delete(review)
    db.session.commit()

    return jsonify({"message": "Review deleted successfully"}), 200



# Edit comment
@book_bp.route('/comments/<int:comment_id>/edit', methods=['PUT'])
@jwt_required()
def edit_comment(comment_id):
    data = request.get_json()
    new_text = data.get('text')

    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    comment = Comment.query.get_or_404(comment_id)

    if comment.user != current_user:
        return jsonify({"error": "You are not authorized to edit this comment"}), 403

    comment.text = new_text
    db.session.commit()

    return jsonify({"message": "Comment edited successfully"}), 200



# Delete comment
@book_bp.route('/comments/<int:comment_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    comment = Comment.query.get_or_404(comment_id)

    if comment.user != current_user:
        return jsonify({"error": "You are not authorized to delete this comment"}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"message": "Comment deleted successfully"}), 200