from pathlib import Path
import duckdb


def main():
    project_root = Path(__file__).resolve().parents[1]
    db_path = project_root / "data" / "feature_engineering.duckdb"
    output_dir = project_root / "outputs"
    output_dir.mkdir(exist_ok=True)

    con = duckdb.connect(str(db_path))

    con.execute("DROP TABLE IF EXISTS user_features")

    con.execute("""
    CREATE TABLE user_features AS
    SELECT
        user_id,
        COUNT(*) AS transaction_count,
        SUM(amount) AS total_spent,
        AVG(amount) AS avg_transaction_amount,
        SUM(CASE WHEN category = 'food' THEN amount ELSE 0 END) AS food_spent,
        SUM(CASE WHEN category = 'tech' THEN amount ELSE 0 END) AS tech_spent,
        SUM(CASE WHEN category = 'travel' THEN amount ELSE 0 END) AS travel_spent,
        SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) AS fraud_count,
        SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END) AS fraud_amount,
        MAX(transaction_time) AS last_transaction_time
    FROM transactions
    GROUP BY user_id;
    """)

    count = con.execute("SELECT COUNT(*) FROM user_features").fetchone()[0]
    print(f"Created user_features table with {count} rows")

    sample = con.execute("""
        SELECT *
        FROM user_features
        ORDER BY total_spent DESC
        LIMIT 10
    """).fetchdf()

    print(sample)

    sample.to_csv(output_dir / "user_features_top10.csv", index=False)
    con.close()


if __name__ == "__main__":
    main()