# Constructs and samples the PyMC change point model.
import pymc as pm
import numpy as np
import pandas as pd
import logging

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
    """
    try:
        summary = pm.summary(idata, var_names=["tau", "mu_1", "mu_2", "sigma"])
        return summary
    except Exception as e:
        logging.error(f"Failed to generate model summary: {e}")
        raise