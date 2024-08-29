from functools import wraps

import jwt
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from modules.middleware import token_required, validate_request_data
from modules.service import login_user_service, register_user_service

app = Flask(__name__)
app.config["SECRET_KEY"] = "4jdHI6oQ5dKVcpzYE1OsnLaEr5gfuz"

# Rate limiting setup
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])


# API endpoint for registering a user
@app.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():
    data = request.get_json()

    # Validate request data using middleware
    validation_result = validate_request_data(
        data, required_fields=["username", "email", "password", "role_id", "first_name"]
    )
    if not validation_result["success"]:
        return jsonify({"message": validation_result["message"]}), 400

    result = register_user_service(data)
    return jsonify({"message": result["message"]}), 201 if result["success"] else 400


# API endpoint for logging in a user
@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()

    # Validate request data using middleware
    validation_result = validate_request_data(data, required_fields=["username", "password"])
    if not validation_result["success"]:
        return jsonify({"message": validation_result["message"]}), 400

    result = login_user_service(data)
    return jsonify({"message": result["message"], "token": result.get("token")}), (
        200 if result["success"] else 401
    )


@app.route("/protected", methods=["GET"])
@token_required
def protected_route(current_user):
    return jsonify(
        {"message": f"Welcome {current_user.username}, your role is {current_user.role}"}
    )


if __name__ == "__main__":
    app.run(debug=True)
