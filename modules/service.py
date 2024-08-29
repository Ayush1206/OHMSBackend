"""
Module for handling user registration services, including validation
and database insertion.
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from werkzeug.security import generate_password_hash

from modules.models import (
    add_employee,
    add_user,
    create_db_session,
    get_user_by_username,
)
from modules.utilities import logger

secret_key = "7U6eFs99l5C4N3SOVyXEBGVurljlC6"


class UserData:
    def __init__(self, username, email, password, role_id, first_name, last_name):
        self.username = username
        self.email = email
        self.password = password
        self.role_id = role_id
        self.first_name = first_name
        self.last_name = last_name


def validate_user_data(user_data):
    """
    Validate the input data for user registration.

    :param user_data: An instance of UserData containing user information.
    :raises ValueError: If any of the inputs are invalid.
    :raises TypeError: If the role_id is not an integer.
    """
    if not all(
        [
            user_data.username,
            user_data.email,
            user_data.password,
            user_data.role_id,
            user_data.first_name,
        ]
    ):
        raise ValueError(
            "All required fields (username, email, password, role_id, first_name) must be provided."
        )
    if len(user_data.username) > 30:
        raise ValueError("Username cannot be longer than 80 characters.")
    if len(user_data.email) > 120:
        raise ValueError("Email cannot be longer than 120 characters.")
    if len(user_data.password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not isinstance(user_data.role_id, int):
        raise TypeError("Role ID must be an integer.")


def decrypt_password(encrypted_password, secret_key):
    """
    Decrypt the encrypted password.

    :param encrypted_password: A dictionary containing the 'iv' and 'content' from the frontend.
    :param secret_key: The secret key used for encryption and decryption.
    :return: The decrypted password as a string.
    """
    try:
        iv = bytes.fromhex(encrypted_password["iv"])
        content = bytes.fromhex(encrypted_password["content"])

        cipher = Cipher(
            algorithms.AES(secret_key.encode()), modes.CBC(iv), backend=default_backend()
        )
        decryptor = cipher.decryptor()

        decrypted_password = decryptor.update(content) + decryptor.finalize()
        return decrypted_password.decode("utf-8").rstrip("\x00")
    except Exception as e:
        logger.error(f"Failed to decrypt password: {e}")
        raise ValueError("Decryption failed")


def register_user_service(data):
    """
    Register a new user in the system.

    :param data: The user data dictionary from the API request.
    :return: A dictionary with the success status and message.
    """
    user_data = UserData(
        username=data["username"],
        email=data["email"],
        password=data["password"],  # Encrypted password
        role_id=data["role_id"],
        first_name=data["first_name"],
        middle_name=data["middle_name"],
        last_name=data["last_name"],
    )

    try:
        # Validate user data
        validate_user_data(user_data)

        # Decrypt the password
        decrypted_password = decrypt_password(user_data.password, secret_key)

        # Hash the password
        hashed_password = generate_password_hash(decrypted_password, method="sha256")

        # Create a session and add user to the database
        session = create_db_session()
        user = add_user(
            session,
            user_data.username,
            user_data.email,
            hashed_password,
            user_data.role_id,
            user_data.first_name,
            user_data.last_name,
            middle_name=data.get("middle_name"),
        )

        # Add employee-specific details if role_id is 1 (employee role)
        if user_data.role_id == 1:
            add_employee(
                session,
                user.id,
                data.get("blood_group"),
                data.get("gov_id"),
                data.get("verification_documents"),
            )

        return {"success": True, "message": "User registered successfully"}

    except (ValueError, TypeError) as exc:
        logger.error(f"Validation error occurred: {exc}")
        return {"success": False, "message": f"Validation error: {exc}"}
    except Exception as exc:
        logger.error(f"An unexpected error occurred: {exc}")
        return {"success": False, "message": f"An unexpected error occurred: {exc}"}


def login_user_service(data):
    """
    Handle user login and generate a JWT token.

    :param data: The user data dictionary from the API request.
    :return: A dictionary with the success status, message, and token.
    """
    try:
        session = create_db_session()
        user = get_user_by_username(session, data["username"])

        if not user or not user.check_password(data["password"]):
            logger.error("Invalid credentials provided.")
            return {"success": False, "message": "Invalid credentials"}

        token = user.generate_token(secret_key="your_secret_key")  # Adjust to use config secret key
        return {"success": True, "message": "Login successful", "token": token}

    except Exception as exc:
        logger.error(f"An unexpected error occurred during login: {exc}")
        return {"success": False, "message": f"An unexpected error occurred: {exc}"}
