### File 4: `tests/test_pipeline.py`
To satisfy the requirement for an explicit validation setup, create a simple test suite using `pytest` to ensure your data structures remain sound:

```python
import pytest
import pandas as pd
import numpy as np

def test_data_loading_schema():
    """Validates that the structured event dataset contains the mandatory columns."""
    try:
        df = pd.read_csv("data/external_events.csv")
    except FileNotFoundError:
        pytest.fail("Missing essential deliverable: data/external_events.csv")
        
    required_columns = ["Event Date", "Event Name", "Description & Market Relevance"]
    for col in required_columns:
        assert col in df.columns, f"Expected column {col} missing from events dataset."
    assert len(df) >= 10, "The events dataset must contain at least 10 key historical events."

def test_log_returns_calculation():
    """Ensures the log return mathematical transformation yields expected properties."""
    mock_prices = pd.Series([10.0, 20.0, 40.0, 20.0])
    log_returns = np.log(mock_prices) - np.log(mock_prices.shift(1))
    
    # First index should be NaN due to differencing shift
    assert pd.isna(log_returns.iloc[0])
    # Doubling price should result in positive log return (~0.693)
    assert np.isclose(log_returns.iloc[1], 0.693147, atol=1e-4)
    # Halving price should result in negative log return (~ -0.693)
    assert np.isclose(log_returns.iloc[3], -0.693147, atol=1e-4)