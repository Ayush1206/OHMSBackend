"""
Module for handling user registration services, including validation
and database insertion.
"""

from werkzeug.security import generate_password_hash

from models import add_employee, add_user


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
            user_data.last_name,
        ]
    ):
        raise ValueError(
            "All required fields (username, email, password, role_id, first_name, last_name) must be provided."
        )
    if len(user_data.username) > 80:
        raise ValueError("Username cannot be longer than 80 characters.")
    if len(user_data.email) > 120:
        raise ValueError("Email cannot be longer than 120 characters.")
    if len(user_data.password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not isinstance(user_data.role_id, int):
        raise TypeError("Role ID must be an integer.")


def register_user_service(
    user_data,
    middle_name=None,
    blood_group=None,
    gov_id=None,
    verification_documents=None,
):
    """
    Register a new user in the system.

    :param user_data: An instance of UserData containing user information.
    :param middle_name: The middle name of the user (optional).
    :param blood_group: The blood group of the user (optional).
    :param gov_id: The government ID of the user (optional).
    :param verification_documents: The verification documents for the user (optional).
    :return: A dictionary with the success status and message.
    """
    try:
        # Validate user data
        validate_user_data(user_data)

        # Hash the password
        hashed_password = generate_password_hash(user_data.password, method="sha256")

        # Add user to the database
        user = add_user(
            user_data.username,
            user_data.email,
            hashed_password,
            user_data.role_id,
            user_data.first_name,
            user_data.last_name,
            middle_name,
        )

        # Add employee-specific details
        if user_data.role_id == 1:  # Assuming role_id 1 corresponds to an employee
            add_employee(user.id, blood_group, gov_id, verification_documents)

        return {"success": True}

    except (ValueError, TypeError) as exc:
        return {
            "success": False,
            "message": f"Validation error occurred: {exc}",
        }
    except Exception as exc:  # pylint: disable=broad-except
        return {
            "success": False,
            "message": f"An unexpected error occurred: {exc}",
        }
