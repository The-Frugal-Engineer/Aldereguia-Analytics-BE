import pandas as pd
import numpy as np

def calculate_investments_montly(total_matrix, invested,initial_investment=0, year='2004'):

    # Set the Date column as the index (optional but useful for datetime operations)
    total_matrix['Date'] = pd.to_datetime(total_matrix['Date'])
    total_matrix.set_index('Date', inplace=True)

    # Filter by start year
    start_year = int(year)
    total_matrix = total_matrix[total_matrix.index.year >= start_year]
    # Keep only the first day of each month
    monthly_matrix = total_matrix.groupby(pd.Grouper(freq='M')).first()

    # Reset the index if needed
    monthly_matrix.reset_index(inplace=True)


    adj_close=monthly_matrix['Adj Close']
    total_invested_array = []
    total_participations_array = []
    total_position_array = []
    total_position=0.0
    total_invested=0.0
    #calculate participations of the initial investment
    if initial_investment > 0:
        first_adj_price=adj_close[0]
        total_position=initial_investment/first_adj_price
    for adj in adj_close:
        total_invested=invested+total_invested
        total_position = (invested / adj) + total_position
        #Add elements to array
        total_participations_array.append(total_position)
        total_position_array.append(total_position *adj)
        total_invested_array.append(total_invested)
        
        

    monthly_matrix['TotalInvested']=total_invested_array
    monthly_matrix['TotalParticipations'] = total_participations_array
    monthly_matrix['TotalPosition'] = total_position_array
    # Display the result
    #monthly_matrix.to_csv("matrix.csv")
    return monthly_matrix



def monte_carlo_simulation_monthly(asset,initial_investment=0 , monthly_investment=1000, T_years=10, N_simulations=1000):
    # Step 1: Download historical asset data
    asset['Date'] = pd.to_datetime(asset['Date'])
    asset.set_index('Date', inplace=True)
    # Step 2: Calculate monthly log returns
    asset['Monthly Return'] = asset['Adj Close'].resample('M').ffill().pct_change()
    asset['Log Returns'] = np.log(1 + asset['Monthly Return'])

    # Step 3: Calculate drift and volatility for monthly returns
    drift = asset['Log Returns'].mean() - (0.5 * asset['Log Returns'].std() ** 2)
    volatility = asset['Log Returns'].std()

    # Step 4: Set up simulation parameters
    T = 12 * T_years  # Time horizon in months
    S0 = asset['Adj Close'][-1]  # Last closing price
    np.random.seed(42)  # For reproducibility

    # Step 5: Monte Carlo simulation
    simulations = np.zeros((T, N_simulations))

    for i in range(N_simulations):
        random_shocks = np.random.normal(0, 1, T)
        price_path = S0 * np.exp(np.cumsum(drift + volatility * random_shocks))
        simulations[:, i] = price_path

    # Step 6: Calculate the average path
    average_path = simulations.mean(axis=1)

    # Step 7: Create a DataFrame with dates and average path
    simulation_dates = pd.date_range(start=asset.index[-1], periods=T + 1, freq='M')[1:]  # Skip the first date
    simulation_dates = simulation_dates + pd.Timedelta(days=1)

    total_invested_array = []
    total_participations_array = []
    total_position_array = []
    total_position = 0.0
    total_invested = 0.0
    #Original investments. Calculate how many stoks I have with my original invesment or position
    if initial_investment>0:
        total_position=initial_investment/S0
    for simulated_value in average_path:
        total_invested = monthly_investment + total_invested
        total_position = (monthly_investment / simulated_value) + total_position
        # Add elements to array
        total_participations_array.append(total_position)
        total_position_array.append(total_position * simulated_value)
        total_invested_array.append(total_invested)

    simulated_results = pd.DataFrame({
        'Date': simulation_dates,
        'TotalInvested': total_invested_array,
        'TotalParticipations': total_participations_array,
        'TotalPosition': total_position_array,


    })



    return simulated_results