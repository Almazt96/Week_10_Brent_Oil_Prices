# Handles loading, cleaning, and log returns.
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """
    Loads Brent oil price historical dataset and handles format conversion.
    Dataset covers May 20, 1987, to September 30, 2022.
    """
    try:
        logging.info(f"Loading data from {file_path}")
        # Expecting columns: 'Date' and 'Price'
        file_path = "./data/raw/BrentOilPrices.csv"
        df = pd.read_csv(file_path)
        
        if 'Date' not in df.columns or 'Price' not in df.columns:
            raise KeyError("Dataset must contain 'Date' and 'Price' columns.")
        
        # Convert date column (Format: day-month-year like 20-May-87)
        df['Date'] = pd.to_datetime(df['Date'], format='mixed')
        # df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='raise')
        df = df.sort_values('Date').reset_index(drop=True)
        
        # Ensure Price is numeric
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        df = df.dropna(subset=['Price'])
        
        logging.info(f"Successfully loaded {len(df)} rows.")
        return df
        
    except FileNotFoundError:
        logging.error(f"File not found at path: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error occurred during data loading/cleaning: {e}")
        raise

def calculate_log_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates log returns: log(price_t) - log(price_t-1) for stationarity.
    """
    try:
        if len(df) < 2:
            raise ValueError("Dataframe must have at least 2 rows to compute returns.")
            
        logging.info("Calculating log returns...")
        df['Log_Price'] = np.log(df['Price'])
        df['Log_Return'] = df['Log_Price'].diff()
        
        # Drop the first NaN row resulting from differencing
        df = df.dropna(subset=['Log_Return']).reset_index(drop=True)
        return df
        
    except Exception as e:
        logging.error(f"Error calculating log returns: {e}")
        raise