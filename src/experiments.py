from pathlib import Path
import duckdb
import time


def run_query(con, sql, label):
    print(f"\n--- {label} ---")
    start = time.time()
    con.execute(sql).fetchall()
    end = time.time()
    print(f"Execution time: {end - start:.5f} seconds")

    explain = con.execute("EXPLAIN " + sql).fetchall()
    print("\nPlan:")
    for k, v in explain:
        print(f"\n{k}\n{v}")


def main():
    project_root = Path(__file__).resolve().parents[1]
    db_path = project_root / "data" / "feature_engineering.duckdb"

    con = duckdb.connect(str(db_path))
    con.execute("SET explain_output = 'all';")

    # Experiment 1: Column pruning
    query1 = """
    SELECT user_id, SUM(amount)
    FROM transactions
    GROUP BY user_id;
    """

    query2 = """
    SELECT *
    FROM transactions;
    """

    run_query(con, query1, "Column Pruning Query (Few columns)")
    run_query(con, query2, "Full Table Scan Query (All columns)")

    # Experiment 2: Selectivity
    query3 = """
    SELECT *
    FROM transactions
    WHERE is_fraud = 1;
    """

    run_query(con, query3, "Selective Filter Query (is_fraud = 1)")

    # Experiment 3: Multi-column aggregation
    query4 = """
    SELECT category, city, SUM(amount)
    FROM transactions
    GROUP BY category, city;
    """

    run_query(con, query4, "Multi-column Aggregation")

    con.close()


if __name__ == "__main__":
    main()