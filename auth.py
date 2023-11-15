from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token
from models import User

auth_bp = Blueprint('auth', __name__)

# Define roles
ROLES = {
    'RegularUser': 1,
    'Administrator': 2,
}

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'RegularUser')  # Default to RegularUser if no role is provided

    # Check if the provided role is valid
    if role not in ROLES:
        return jsonify({"error": "Invalid role"}), 400

    # Check if the user already exists
    if User.get_user_by_username(username=username) is not None:
        return jsonify({"error": "User already exists"}), 403

    new_user = User(
        username=username,
        email=email,
        role=ROLES[role],  # Assign the role
    )
    new_user.set_password(password=password)
    new_user.save()

    return jsonify({"message": "User created"}), 201

@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.get_user_by_username(username=username)

    if user and user.check_password(password=password):
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        return jsonify(
            {"message": "Logged In ",
             "tokens": {
                 "access": access_token,
                 "refresh": refresh_token
             },
                "role": user.role,
                "user_id": user.id
             }
        ), 200

    return jsonify({"error": "Invalid username or password"}), 400
