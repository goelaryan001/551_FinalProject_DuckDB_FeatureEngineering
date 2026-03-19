# 551_FinalProject_DuckDB_FeatureEngineering
# 🦆 DuckDB Feature Engineering Pipeline

This project explores **DuckDB** as an embedded analytical database and demonstrates how its internal design — particularly **columnar storage** and **vectorized execution** — impacts the performance of feature engineering workloads.

The system simulates a realistic data pipeline where transactional data is transformed into user-level features, and the internal behavior of DuckDB is analyzed using execution plans and experiments.

---

## 🚀 Project Highlights

- Embedded DuckDB database (no server required)
- Synthetic transactional dataset generation
- Feature engineering using SQL
- Execution plan analysis (`EXPLAIN`, `EXPLAIN ANALYZE`)
- Benchmark experiments (scan vs aggregation vs filtering)
- Interactive Streamlit dashboard
- Mapping database internals to application behavior

---

## 📁 Project Structure
├── app/
│ └── streamlit_app.py
├── data/
│ └── feature_engineering.duckdb
├── raw_data/
│ └── transactions.csv
├── outputs/
│ ├── benchmark_results.csv
│ ├── explain_user_features.txt
│ ├── user_features_top10.csv
│ └── user_features_top20.csv
├── src/
│ ├── generate_data.py
│ ├── setup_db.py
│ ├── run_features.py
│ ├── build_feature_table.py
│ └── benchmark_queries.py
├── requirements.txt
└── README.md


---

## ⚙️ Requirements

- Python 3.10+
- DuckDB
- Pandas
- NumPy
- Streamlit
- PyArrow

---

## 🧪 Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd <repo-name>

2. Create a virtual environment
macOS / Linux
python3 -m venv venv
source venv/bin/activate
Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
Windows (CMD)
python -m venv venv
venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt

If needed:

pip install duckdb pandas numpy streamlit pyarrow
▶️ How to Run the Project
Step 1: Generate dataset
python src/generate_data.py

Creates:

raw_data/transactions.csv
Step 2: Load data into DuckDB
python src/setup_db.py

Creates:

data/feature_engineering.duckdb
Step 3: Run feature queries
python src/run_features.py

Outputs:

Feature results

Execution plan

Query profiling

Step 4: Build feature table
python src/build_feature_table.py
Step 5: Run experiments
python src/benchmark_queries.py

Creates:

outputs/benchmark_results.csv
Step 6: Launch Streamlit app
streamlit run app/streamlit_app.py

Open:

http://localhost:8501
🧠 What This Project Does

This project simulates a feature engineering pipeline over transactional data.

Features Computed:

Total transaction value

Transaction count

Average transaction amount

Fraud metrics

Merchant diversity

Category diversity

User activity (time-based)

🧩 DuckDB Internals Explored
Columnar Storage

DuckDB scans only required columns (column pruning).

Vectorized Execution

DuckDB processes data in batches using operators such as:

SEQ_SCAN

HASH_GROUP_BY

TOP_N

🧪 Experiments Conducted

Narrow aggregation queries

Full table scans

Selective filtering (is_fraud)

Multi-column aggregation

Point lookup queries

📊 Key Observations

Narrow queries are significantly faster than wide queries

DuckDB avoids scanning unnecessary columns

Aggregation queries are efficient

Scan-based execution works well for OLAP workloads