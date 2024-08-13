from flask import Flask, request, jsonify
from service import register_user_service
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# API endpoint for registering a user
@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.get_json()

    # Extract the data from the request
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id')
    first_name = data.get('first_name')
    middle_name = data.get('middle_name', None)
    last_name = data.get('last_name')
    blood_group = data.get('bloodgroup', None)
    gov_id = data.get('govid', None)
    verification_documents = data.get('verificationdocuments', None)

    # Call the service function to register the user
    result = register_user_service(username, email, password, role_id, first_name, last_name, middle_name, blood_group, gov_id, verification_documents)

    if result['success']:
        return jsonify({'message': 'User registered successfully!'}), 201
    else:
        return jsonify({'message': result['message']}), 400

# API endpoint for logging in a user
@app.route('/login_user', methods=['POST'])
def login_user():
    data = request.get_json()

    # Here you would implement your login logic, including checking the password hash, etc.
    # This is just a placeholder example:
    email = data.get('email')
    password = data.get('password')

    # Retrieve user from the database (pseudo-code)
    user = get_user_by_email(email)

    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

if __name__ == '__main__':
    app.run(debug=True)
