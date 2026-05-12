import re
from flask import Blueprint, render_template, request, jsonify

from app.extensions import database
from app.database_utils.user_database_utils import check_user_exists_by_username, create_user
from app.models.user import User

register_bp = Blueprint("register", __name__)

@register_bp.route('/register', methods=["GET", "POST"])
def register():
    """Register route"""
    
    if request.method == "GET":

        return render_template('register.html')
    

    elif request.method == "POST":
        # Data extraction
        data = request.get_json()
        username = data.get('username', None)
        password = data.get('password', None)
        email = data.get('email', None)


        # Validation
        if not username:
            return jsonify({"error": "Username is required."}), 400
        if not email:
            return jsonify({"error": "Email is required."}), 400
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return jsonify({"error": "Please enter a valid email address."}), 400
        if not password:
            return jsonify({"error": "Password is required."}), 400
        
        # Password validation (minimum 8 characters)
        if len(password) < 8:
            return jsonify({"error": "Password must be at least 8 characters long."}), 400
        
        if check_user_exists_by_username(database, username):
            return jsonify({"error": "Username already exists."}), 400
        

        # Create new user
        new_user = User(username=username, password=password, email=email)
        new_user.hash_password(password)  # Hash the password before storing
        create_user(database, new_user)

        return jsonify({"message": "User created successfully."}), 201