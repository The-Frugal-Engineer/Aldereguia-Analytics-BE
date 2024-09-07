from calculations import calculate_investments_montly, monte_carlo_simulation_monthly

from files import read_csv_to_panda
from flask import Flask, jsonify, request, Response
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

USERNAME = 'dartfordmadrid'
PASSWORD = 'dartfordmadrid'


def check_auth(username, password):
    """Check if a username/password combination is valid."""
    return username == USERNAME and password == PASSWORD


def authenticate():
    """Sends a 401 response that enables basic auth."""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route("/calculations", methods=["POST"])
@requires_auth
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


