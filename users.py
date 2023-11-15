

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
from extensions import db

user_bp = Blueprint('user', __name__)

# Edit user role
@user_bp.route('/users/<string:user_id>/edit-role', methods=['PUT'])
@jwt_required()
def edit_user_role(user_id):
    
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    if current_user.role != '2' and current_user.id != user_id:
        return jsonify({"error": "You are not authorized to perform this action"}), 403

    
    user_to_edit = User.query.get_or_404(user_id)

    data = request.get_json()
    new_role = data.get('role')

 
    user_to_edit.role = new_role
    db.session.commit()

    return jsonify({"message": "User role edited successfully"}), 200


# Delete user
@user_bp.route('/users/<string:user_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    if current_user.role != '2' and current_user.id != user_id:
        return jsonify({"error": "You are not authorized to perform this action"}), 403

    # Retrieve the user to be deleted
    user_to_delete = User.query.get_or_404(user_id)

    # Delete the user
    db.session.delete(user_to_delete)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200
