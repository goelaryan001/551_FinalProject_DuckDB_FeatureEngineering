from pathlib import Path
import duckdb


def print_plan(con, sql: str, analyze: bool = False) -> str:
    prefix = "EXPLAIN ANALYZE " if analyze else "EXPLAIN "
    rows = con.execute(prefix + sql).fetchall()

    lines = []
    for key, value in rows:
        header = f"\n{'=' * 100}\n{key}\n{'=' * 100}"
        lines.append(header)
        lines.append(value)

    text = "\n".join(lines)
    print(text)
    return text


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
        MIN(transaction_time) AS first_transaction_time,
        MAX(transaction_time) AS last_transaction_time,
        SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) AS fraud_count,
        SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END) AS fraud_amount,
        COUNT(DISTINCT merchant_id) AS unique_merchants,
        COUNT(DISTINCT category) AS category_diversity,
        COUNT(DISTINCT DATE(transaction_time)) AS active_days
    FROM transactions
    GROUP BY user_id;
    """)

    df = con.execute("""
        SELECT *
        FROM user_features
        ORDER BY total_spent DESC
        LIMIT 10
    """).fetchdf()

    print(df)
    df.to_csv(output_dir / "user_features_top10.csv", index=False)
    con.close()


if __name__ == "__main__":
    main()