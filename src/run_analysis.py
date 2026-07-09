# Main execution script linking data processing, modeling, and output extraction.
# Main execution script linking data processing, modeling, and output extraction.
import os
import pandas as pd
import numpy as np
from src.data_processing import load_and_clean_data, calculate_log_returns
from src.bayesian_modeling import build_and_sample_change_point_model, extract_summary_metrics, export_analysis_results

def main():
    # Configure path to your historical dataset
    DATA_PATH = "data/processed/historical_prices.csv" 
    DATA_FOLDER = "d:/Personal/Kifiya 10 Academy/10 Academy/Week_10_Brent_Oil_Prices/data"
    
    if not os.path.exists(DATA_PATH):
        print(f"[Error] Please place your dataset at {DATA_PATH} or update the path variables.")
        return

    try:
        # Step 1: Process Data
        df = load_and_clean_data(DATA_PATH)
        df_with_returns = calculate_log_returns(df)
        
        # Step 2: Extract target array for modeling (e.g., using Price or Log Returns)
        prices_array = df_with_returns['Price'].values
        dates_array = df_with_returns['Date'].values
        
        # Step 3: Run Change Point Model
        model, idata = build_and_sample_change_point_model(prices_array, draws=1500, tune=1000)
        
        # Step 4: Evaluate Output & Convergence
        summary = extract_summary_metrics(idata)
        print("\n=== Model Posterior Summary ===")
        print(summary)
        
        # Step 5: Pinpoint the Change Point Date
        # Fetch the mean index of posterior tau
        posterior_tau = idata.posterior["tau"].values.flatten()
        estimated_index = int(np.round(np.mean(posterior_tau)))
        
        # Safety index guard check
        estimated_index = min(max(0, estimated_index), len(dates_array) - 1)
        
        # Fetch the actual timestamp from our data array
        detected_date = pd.to_datetime(dates_array[estimated_index])
        
        # Fix: Enforce numerical conversion directly using pd.to_numeric to allow calculations
        mu1_val = float(pd.to_numeric(summary.loc["mu_1", "mean"]))
        mu2_val = float(pd.to_numeric(summary.loc["mu_2", "mean"]))

        # Calculate percentage shift seamlessly now using float values
        pct_change = ((mu2_val - mu1_val) / mu1_val) * 100
        
        print("\n=== Quantitative Insight Statement ===")
        print(f"The model detects a prominent structural change point around {detected_date.strftime('%Y-%m-%d')}.")
        print(f"The average daily oil price shifted from ${mu1_val:.2f} to ${mu2_val:.2f}, representing a change of {pct_change:.2f}%.")
        
        # Step 6: Export results into your unified data folder for your Flask server
        print("\n=== Exporting Data Files ===")
        export_analysis_results(df_with_returns, idata, summary, output_dir=DATA_FOLDER)
        print("Done! Web dashboard assets updated successfully.")
        
    except Exception as e:
        print(f"\nExecution failed due to an unhandled exception: {e}")

if __name__ == "__main__":
    main()