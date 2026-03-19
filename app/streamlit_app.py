from pathlib import Path
import duckdb
import streamlit as st
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "feature_engineering.duckdb"


st.set_page_config(page_title="DuckDB Feature Engineering", layout="wide")
st.title("DuckDB Feature Engineering Demo")

if not DB_PATH.exists():
    st.error("Database not found. Run src/setup_db.py first.")
    st.stop()

con = duckdb.connect(str(DB_PATH))

st.sidebar.header("Controls")
user_id = st.sidebar.number_input("User ID", min_value=1, value=1, step=1)
limit_n = st.sidebar.slider("Top N users", min_value=5, max_value=100, value=20)

feature_sql = f"""
SELECT
    user_id,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_spent,
    AVG(amount) AS avg_transaction_amount,
    MAX(transaction_time) AS last_transaction_time
FROM transactions
GROUP BY user_id
ORDER BY total_spent DESC
LIMIT {limit_n};
"""

if st.button("Run feature query"):
    st.subheader("Feature query result")
    df = con.execute(feature_sql).fetchdf()
    st.dataframe(df, use_container_width=True)

    st.subheader("EXPLAIN plan")
    explain_df = con.execute("EXPLAIN " + feature_sql).fetchdf()
    st.dataframe(explain_df, use_container_width=True)

st.divider()

st.subheader(f"Transactions for user {user_id}")
user_txn_df = con.execute(
    "SELECT * FROM transactions WHERE user_id = ? ORDER BY transaction_time DESC LIMIT 20",
    [user_id]
).fetchdf()

st.subheader("Fraud Analysis")

fraud_df = con.execute("""
SELECT category, city, COUNT(*) AS fraud_cases
FROM transactions
WHERE is_fraud = 1
GROUP BY category, city
ORDER BY fraud_cases DESC
LIMIT 20
""").fetchdf()

st.dataframe(fraud_df)

st.dataframe(user_txn_df, use_container_width=True)

con.close()