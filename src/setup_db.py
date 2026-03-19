from pathlib import Path
import duckdb


def main():
    project_root = Path(__file__).resolve().parents[1]
    raw_csv = project_root / "raw_data" / "transactions.csv"
    db_path = project_root / "data" / "feature_engineering.duckdb"

    db_path.parent.mkdir(exist_ok=True)

    con = duckdb.connect(str(db_path))

    con.execute("DROP TABLE IF EXISTS transactions")

    create_sql = f"""
    CREATE TABLE transactions AS
    SELECT *
    FROM read_csv_auto('{raw_csv.as_posix()}');
    """
    con.execute(create_sql)

    row_count = con.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    print(f"Loaded {row_count} rows into DuckDB database at {db_path}")

    sample = con.execute("""
        SELECT *
        FROM transactions
        LIMIT 5
    """).fetchdf()

    print("\nSample rows:")
    print(sample)

    con.close()


if __name__ == "__main__":
    main()