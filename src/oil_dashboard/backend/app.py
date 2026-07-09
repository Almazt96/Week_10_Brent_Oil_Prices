from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Allows React frontend to fetch data

# --- Data Configuration ---
DATA_FOLDER = 'd:/Personal/Kifiya 10 Academy/10 Academy/Week_10_Brent_Oil_Prices/data/processed'  # Ensure this path matches your analysis output folder

def get_csv_data(filename):
    """Safely loads generated CSV results into memory for the API endpoints."""
    file_path = os.path.join(DATA_FOLDER, filename)
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.lower()  # keep keys lowercase for frontend consistency
            return df.to_dict(orient='records')
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return []
    print(f"File not found: {file_path}. Please run your analysis script first.")
    return []

# --- API Endpoints dynamically reading your data folder ---

@app.route('/api/historical-prices', methods=['GET'])
def get_historical_prices():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Dynamically loads your PyMC generated historical outputs
    historical_data = get_csv_data('historical_prices.csv')
    filtered_data = historical_data
    
    if start_date or end_date:
        filtered_data = []
        for row in historical_data:
            try:
                row_date = datetime.strptime(str(row['date']), '%Y-%m-%d')
                if start_date and row_date < datetime.strptime(start_date, '%Y-%m-%d'):
                    continue
                if end_date and row_date > datetime.strptime(end_date, '%Y-%m-%d'):
                    continue
                filtered_data.append(row)
            except (ValueError, KeyError):
                continue  # Skip missing or corrupted row rows gracefully
            
    return jsonify({
        "status": "success",
        "count": len(filtered_data),
        "data": filtered_data
    })

@app.route('/api/change-points', methods=['GET'])
def get_change_points():
    # Dynamically loads your PyMC generated change points
    change_points = get_csv_data('change_points.csv')
    return jsonify({
        "status": "success",
        "data": change_points
    })

@app.route('/api/event-correlations', methods=['GET'])
def get_event_correlations():
    # Dynamically loads structural event information matching dates
    event_correlations = get_csv_data('event_correlations.csv')
    return jsonify({
        "status": "success",
        "data": event_correlations
    })

@app.route('/api/prices')
def get_prices():
    historical_data = get_csv_data('historical_prices.csv')
    return jsonify({
        "status": "success", 
        "data": historical_data[:100]  # sample of first 100 rows
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)