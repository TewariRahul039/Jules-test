from flask import Blueprint, jsonify, request, current_app
import jwt
from datetime import datetime, timedelta, timezone

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400

    # In a real application, you would add the user to the database here.
    # For this stub, we just simulate success.
    username = data.get('username')
    return jsonify({'message': f'User {username} registered successfully (stub)'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400

    username = data.get('username')
    password = data.get('password')

    # Mock authentication
    if username == "testuser" and password == "password":
        token_payload = {
            'user_id': 1, # Dummy user ID
            'username': 'testuser',
            'exp': datetime.now(timezone.utc) + timedelta(hours=1) # Token expires in 1 hour
        }

        try:
            token = jwt.encode(
                token_payload,
                current_app.config['SECRET_KEY'],
                algorithm=current_app.config['JWT_ALGORITHM']
            )
            return jsonify({'message': 'Login successful (stub)', 'token': token}), 200
        except Exception as e:
            return jsonify({'message': f'Error generating token: {str(e)}'}), 500
    else:
        return jsonify({'message': 'Invalid credentials (stub)'}), 401
