<!-- Task 1a Data Science Workflow
1. Planned Data Analysis Workflow
To evaluate how macroeconomic factors, geopolitical friction, and structural shifts impact Brent crude prices, we follow a rigorous, four-tiered data science workflow: 
[Data Ingestion & Cleaning] ➔ [Exploratory Data Analysis] ➔ [Bayesian Change Point Modelling] ➔ [Insight & Dashboard Deployment]
•	Data Ingestion & Cleaning: Load historical daily Brent crude price data spanning May 20, 1987, to September 30, 2022. Standardize date strings (DD-MMM-YY) into structural datetime formats and sweep for missing or invalid observations. 
•	Exploratory Data Analysis (EDA): Perform rolling trend tracking, isolate volatility clusters, and apply log-transformations to evaluate the statistical properties of the series. 
•	Bayesian Change Point Modelling: Implement a Markov Chain Monte Carlo (MCMC) sampler via PyMC using a discrete uniform prior (tau) to identify distinct statistical regime shifts in the historical price mean. 
•	Causal Mapping & Reporting: Correlate identified mathematical structural breaks against a curated database of real-world geopolitical events to quantify localized market responses.  -->
