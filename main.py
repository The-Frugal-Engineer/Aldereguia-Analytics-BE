from calculations import calculate_investments_montly, monte_carlo_simulation_monthly

from files import read_csv_to_panda
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity



app = Flask(__name__)
CORS(app)

USERNAME = 'dartfordmadrid'
PASSWORD = 'dartfordmadrid'

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'  # Change this in production

# Initialize JWT Manager
jwt = JWTManager(app)



@app.route("/calculations", methods=["POST"])
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


