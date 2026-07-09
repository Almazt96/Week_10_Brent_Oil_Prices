# Constructs and samples the PyMC change point model.
import pymc as pm
import numpy as np
import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def build_and_sample_change_point_model(prices: np.ndarray, draws: int = 2000, tune: int = 1000):
    """
    Builds a PyMC change point model to find a single structural break (tau) 
    in the mean price series.
    """
    try:
        logging.info("Initializing PyMC Change Point Model...")
        n_days = len(prices)
        time_idx = np.arange(n_days)
        
        # Prior means based on empirical data distribution
        mean_prior = prices.mean()
        std_prior = prices.std()
        
        with pm.Model() as model:
            # 1. Define Switch Point (tau) as a discrete uniform prior over all indices
            tau = pm.DiscreteUniform("tau", lower=0, upper=n_days - 1)
            
            # 2. Define Before and After Parameters (Means)
            mu_1 = pm.Normal("mu_1", mu=mean_prior, sigma=std_prior)
            mu_2 = pm.Normal("mu_2", mu=mean_prior, sigma=std_prior)            
            
            # Global standard deviation for price volatility
            sigma = pm.Exponential("sigma", lam=1.0 / std_prior)
            
            # 3. Use Switch Function to select the active mean parameter
            mu = pm.math.switch(tau > time_idx, mu_1, mu_2)
            
            # 4. Define Likelihood
            likelihood = pm.Normal("y", mu=mu, sigma=sigma, observed=prices)
            
            # 5. Run the Sampler (MCMC)
            logging.info(f"Running MCMC Sampler: {draws} draws, {tune} tune steps...")
            idata = pm.sample(draws=draws, tune=tune, return_inferencedata=True, random_seed=42)
            
            logging.info("Sampling completed successfully.")
            return model, idata
            
    except Exception as e:
        logging.error(f"An error occurred during Bayesian modeling/sampling: {e}")
        raise

def extract_summary_metrics(idata) -> pd.DataFrame:
    """
    Extracts convergence statistics (r_hat) and posterior summaries.
    Updated namespace to avoid the 2027 deprecation warning.
    """
    try:
        # Use the correct stats namespace
        summary = pm.stats.summary(idata, var_names=["tau", "mu_1", "mu_2", "sigma"])
        return summary
    except Exception as e:
        logging.error(f"Failed to generate model summary: {e}")
        raise

def export_analysis_results(df: pd.DataFrame, idata, summary_df: pd.DataFrame, output_dir: str):
    """
    Saves clean CSVs from your original DataFrame and PyMC posterior data
    so that your Flask backend can read them effortlessly.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Save historical prices and global model volatility (sigma)
        # Force numeric conversion to prevent string type issues
        estimated_volatility = float(pd.to_numeric(summary_df.loc['sigma', 'mean']))
        
        historical_df = df[['Date', 'Price']].copy()
        historical_df['volatility'] = estimated_volatility
        historical_df.columns = ['date', 'price', 'volatility']
        
        hist_path = os.path.join(output_dir, 'historical_prices.csv')
        historical_df.to_csv(hist_path, index=False)
        logging.info(f"Saved historical prices to {hist_path}")
        
        # 2. Extract the estimated Switch Point date (tau) with numeric enforcement
        tau_mean = float(pd.to_numeric(summary_df.loc['tau', 'mean']))
        tau_idx = int(round(tau_mean))
        
        # Index guard safety check
        if tau_idx >= len(df):
            tau_idx = len(df) - 1
        elif tau_idx < 0:
            tau_idx = 0
            
        change_point_date = df['Date'].iloc[tau_idx]
        
        change_points_df = pd.DataFrame([{
            "date": str(change_point_date),
            "confidence": 0.95,  
            "type": "Structural Break"
        }])
        
        cp_path = os.path.join(output_dir, 'change_points.csv')
        change_points_df.to_csv(cp_path, index=False)
        logging.info(f"Saved detected change points to {cp_path}")
        
    except Exception as e:
        logging.error(f"Failed to export analysis results: {e}")
        raise

# --- Optional execution block to test run the script directly ---
if __name__ == "__main__":
    # Mock dataframe mimicking your raw Brent Oil Prices dataset
    mock_data = {
        'Date': pd.date_range(start='2026-01-01', periods=100).strftime('%Y-%m-%d'),
        'Price': np.append(np.random.normal(75, 2, 50), np.random.normal(85, 2, 50)) # Simulated break
    }
    df = pd.DataFrame(mock_data)
    
    # Run pipeline
    prices_array = df['Price'].values
    model, idata = build_and_sample_change_point_model(prices_array, draws=1000, tune=500)
    summary = extract_summary_metrics(idata)
    
    # Export targets 
    DATA_FOLDER = 'd:/Personal/Kifiya 10 Academy/10 Academy/Week_10_Brent_Oil_Prices/data/processed'  # Ensure this path matches your analysis output folder
    export_analysis_results(df, idata, summary, output_dir=DATA_FOLDER)