# This file contains routes for administrator functionalities.
# admin can edit user role and delete but that in users.py file 
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Review, Comment
from extensions import db


admin_bp = Blueprint('admin', __name__)


# Get all reviews 
@admin_bp.route('/reviews', methods=['GET'])
@jwt_required()
def get_all_reviews():
    # current user has administrator role
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    if current_user.role != '2':
        return jsonify({"error": "You are not authorized to perform this action"}), 403

    # Retrieve all reviews from the database
    reviews = Review.query.all()

    reviews_list = []
    for review in reviews:
        comments = Comment.query.filter_by(review_id=review.id).all()

        review_details = {
            "id": review.id,
            "rating": review.rating,
            "text": review.text,
            "created_at": review.created_at,
            "user": {
                "id": review.user.id,
                "username": review.user.username,
                "email": review.user.email,
            },
            "book": {
                "id": review.book.id,
                "title": review.book.title,
                "author": review.book.author,
            },
            "comments": [
                {
                    "id": comment.id,
                    "text": comment.text,
                    "created_at": comment.created_at,
                    "user": {
                        "id": comment.user.id,
                        "username": comment.user.username,
                        "email": comment.user.email,
                    }
                }
                for comment in comments
            ]
        }

        reviews_list.append(review_details)

    return jsonify({"reviews": reviews_list}), 200


# Edit review
@admin_bp.route('/reviews/<int:review_id>/edit', methods=['PUT'])
@jwt_required()
def edit_review(review_id):
    
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    if current_user.role != '2':
        return jsonify({"error": "You are not authorized to perform this action"}), 403

    
    review_to_edit = Review.query.get_or_404(review_id)

    data = request.get_json()
    new_text = data.get('text')

    review_to_edit.text = new_text
    db.session.commit()

    return jsonify({"message": "Review edited successfully"}), 200



# Delete review 
@admin_bp.route('/reviews/<int:review_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    if current_user.role != '2':
        return jsonify({"error": "You are not authorized to perform this action"}), 403

    review_to_delete = Review.query.get_or_404(review_id)#delete review


    db.session.delete(review_to_delete)
    db.session.commit()

    return jsonify({"message": "Review deleted successfully"}), 200


# Edit comment
@admin_bp.route('/comments/<int:comment_id>/edit', methods=['PUT'])
@jwt_required()
def edit_comment(comment_id):
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    if current_user.role != '2':
        return jsonify({"error": "You are not authorized to perform this action"}), 403

    comment_to_edit = Comment.query.get_or_404(comment_id)


    data = request.get_json()
    new_text = data.get('text')

    comment_to_edit.text = new_text
    db.session.commit()

    return jsonify({"message": "Comment edited successfully"}), 200


# Delete comment
@admin_bp.route('/comments/<int:comment_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    if current_user.role != '2':
        return jsonify({"error": "You are not authorized to perform this action"}), 403

    comment_to_delete = Comment.query.get_or_404(comment_id)

    db.session.delete(comment_to_delete)
    db.session.commit()

    return jsonify({"message": "Comment deleted successfully"}), 200
