# Analysis Pipeline & Modeling Workflow

This document outlines the end-to-end data processing, modeling, and evaluation pipeline used in this project.

### 1. Data Ingestion & Preprocessing
* **Sources:** Historical Brent Crude/WTI price data (`data/raw/`) and compiled event data (`data/events.csv`).
* **Processing:** Date-time alignment, handling missing values via interpolation, and calculating log returns.

### 2. Time-Series Exploratory Data Analysis (EDA)
* Automated stationarity testing (ADF, KPSS) to determine the integration order.
* Volatility modeling (GARCH processes) to identify regime clusters.
* **Impact on Modeling:** Because commodity prices exhibit high volatility clustering and structural breaks, we utilize a Bayesian Change Point model (e.g., PyMC or Ruptures with a Bayesian framework) rather than standard linear assumptions.

### 3. Bayesian Change Point Modeling (BCPM)
* **Priors:** We model change points using a Poisson process for transition frequency and normal/gamma distributions for segment means/volatilities.
* **MCMC Sampling:** Using PyMC to sample the posterior distribution of change point locations ($t_i$).
* **Output:** Posterior probabilities of change points mapped against historical timelines.

### 4. Causal Narrative & Validation
* Change points are automatically aligned with the window $[t_i - \delta, $t_i + \delta]$ of the registered `events.csv` to calculate the statistical significance of price/volatility shifts following key events.