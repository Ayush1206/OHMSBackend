"""
Module for middleware functions, such as input validation and authentication.
"""

from functools import wraps

import jwt
from flask import jsonify, request

from modules.models import Users, create_db_session
from modules.utilities import logger


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            logger.warning("Token is missing in the request.")
            return jsonify({"message": "Token is missing!"}), 403

        try:
            data = jwt.decode(
                token, "your_secret_key", algorithms=["HS256"]
            )  # Adjust to use config secret key
            session = create_db_session()
            current_user = session.query(Users).filter_by(id=data["id"]).first()
            if current_user is None:
                raise ValueError("User not found")
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired.")
            return jsonify({"message": "Token has expired!"}), 403
        except Exception as exc:
            logger.error(f"Token is invalid: {exc}")
            return jsonify({"message": f"Token is invalid: {exc}"}), 403

        return f(current_user, *args, **kwargs)

    return decorated


def validate_request_data(data, required_fields):
    """
    Validate that the required fields are present in the request data.

    :param data: The request data dictionary.
    :param required_fields: A list of required fields to check.
    :return: A dictionary with the validation result and message.
    """
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        logger.warning(f"Missing required fields: {missing_fields}")
        return {
            "success": False,
            "message": f"Missing required fields: {', '.join(missing_fields)}",
        }
    return {"success": True}
