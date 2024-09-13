from calculations import calculate_investments_montly, monte_carlo_simulation_monthly

from files import read_csv_to_panda
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'dartfordmadrid001'
app.config['JWT_SECRET_KEY'] = 'dartfordmadrid001'  # Change this in production

# Set the JWT token expiration to 24 hours
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize JWT Manager
jwt = JWTManager(app)

users = {
    'alex@example.com': {'password': 'fossil'},
    'ruben@example.com': {'password': 'fluorine'},
    'pablo@example.com': {'password': 'tennis'},
    'alex@alex.com': {'password': 'fishing'}

}

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    # Authenticate User
    if email not in users or users[email]['password'] != password:
        return jsonify({"msg": "Invalid credentials"}), 401

    # Create JWT Token
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "Invalid token"}), 422

@jwt.invalid_token_loader
def missing_token_callback(error):
    return jsonify({"error": "Token is missing"}), 401


@app.route("/calculations", methods=["POST"])
@jwt_required()
def get_example():
    # Retrieve JSON data from the request
    jsonrequest = request.get_json()

    param = request.args.get('param')
    datajson = request.get_json(param)
    print("Received data:", datajson)

    amount = jsonrequest.get('amount')
    year = jsonrequest.get('year')
    ticker = jsonrequest.get('ticker')
    simulation_type = jsonrequest.get('simulation_type')
    initial_investment = jsonrequest.get('initial_investment')

    try:
        amount = int(amount)
        year = int(year)
        initial_investment = int(initial_investment)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid parameter. Please provide an integer."}), 400

    total_matrix = read_csv_to_panda(ticker)
    if simulation_type == "past":
        monthly_matrix=calculate_investments_montly(total_matrix, amount,initial_investment, year)
    else:
        monthly_matrix = monte_carlo_simulation_monthly(total_matrix,initial_investment , amount, year)
    response = jsonify(monthly_matrix.to_dict())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response  # Convert DataFrame to dict and return as JSON


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


