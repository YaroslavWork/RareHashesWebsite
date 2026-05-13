from flask import Blueprint, render_template, request, jsonify
from flask_login import login_user

from app.extensions import database
from app.database_utils.user_database_utils import check_user_credentials, get_user_by_username

login_bp = Blueprint("login", __name__)

@login_bp.route('/login', methods=["GET", "POST"])
def login():
    """Login route"""
    
    if request.method == "GET":

        return render_template('login.html')
    
    elif request.method == "POST":
        # Data extraction
        data = request.get_json()
        username = data.get('username', None)
        password = data.get('password', None)

        # Validation
        if not username:
            return jsonify({"error": "Username is required."}), 400
        if not password:
            return jsonify({"error": "Password is required."}), 400
        
        if not check_user_credentials(database, username, password):
            return jsonify({"error": "Invalid username or password."}), 401

        user = get_user_by_username(database, username)
        print(user)
        login_user(user)  # Log the user in using Flask-Login

        return jsonify({"message": "Login successful."}), 200