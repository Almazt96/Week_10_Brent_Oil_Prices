Task 1a Correlation vs. Causation write-up
4. Modeling Assumptions and Limitations
Core System Assumptions
1.	Regime Abruptness: The baseline change point model assumes structural breaks occur rapidly at a specific time step (tau), rather than modelling slow, multi-month economic transitions. 
2.	Parameter Isolation: We assume structural breaks are primarily captured through shifts in the mean price (mu_1, mu_2), supported by an exponentially distributed global variance parameter (sigma). 
Analytical Limitations & The Correlation vs. Causation Divide
A primary limitation of this framework is the fundamental difference between establishing a statistical correlation in time versus proving an absolute causal impact. 
Critical Methodological Note: If the PyMC model isolates a sharp posterior probability peak for a change point around March 2020, the mathematics only proves that the data's underlying probability distribution altered significantly at that index. It cannot see the external world. Attributing that shift to the OPEC+ price war or COVID-19 lockdowns requires qualitative domain expertise and comparative contextual mapping. Correlation shows when the market shifted; historical policy analysis explains why.