# Week_10_Brent_Oil_Prices
# Brent Crude Oil Price Analysis Dashboard

## Data Source & Expected Location
The analysis relies on the historical daily Brent crude oil price dataset spanning May 20, 1987, to September 30, 2022 (recorded in USD per barrel).
* **Source:** Provided via Birhan Energies consultancy data records / 10 Academy portal.
* **Expected Location:** Place the raw source file at `data/raw/brent_prices.csv` before running the data pipelines.

## Local Installation & Environment Setup
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <your-repo-link>
   cd repository-name
   
An interactive full-stack data analytics dashboard mapping historical crude oil anomalies against defining global events (conflicts, policy shifts, sanctions).

## System Architecture
- **Backend**: Python Flask REST API 
- **Frontend**: React.js with Recharts (Data Visualizations)

---

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js (v16+)

### 1. Backend Setup (Flask)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
python app.py