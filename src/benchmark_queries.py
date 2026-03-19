from pathlib import Path
import duckdb
import time
import csv


QUERIES = {
    "narrow_aggregation": """
        SELECT user_id, SUM(amount)
        FROM transactions
        GROUP BY user_id;
    """,
    "wide_scan": """
        SELECT *
        FROM transactions;
    """,
    "selective_filter": """
        SELECT *
        FROM transactions
        WHERE is_fraud = 1;
    """,
    "multi_column_groupby": """
        SELECT category, city, SUM(amount)
        FROM transactions
        GROUP BY category, city;
    """,
    "point_lookup": """
        SELECT *
        FROM transactions
        WHERE user_id = 100;
    """
}


def time_query(con, sql, repeats=5):
    con.execute(sql).fetchall()  # warmup
    times = []
    row_count = None

    for _ in range(repeats):
        start = time.perf_counter()
        rows = con.execute(sql).fetchall()
        end = time.perf_counter()
        times.append(end - start)
        row_count = len(rows)

    return sum(times) / len(times), row_count


def main():
    project_root = Path(__file__).resolve().parents[1]
    db_path = project_root / "data" / "feature_engineering.duckdb"
    out_path = project_root / "outputs" / "benchmark_results.csv"
    out_path.parent.mkdir(exist_ok=True)

    con = duckdb.connect(str(db_path))

    results = []
    for name, sql in QUERIES.items():
        avg_time, row_count = time_query(con, sql)
        results.append({
            "query_name": name,
            "avg_seconds": round(avg_time, 6),
            "row_count": row_count
        })
        print(f"{name}: {avg_time:.6f}s, rows={row_count}")

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["query_name", "avg_seconds", "row_count"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nSaved benchmark results to {out_path}")
    con.close()


if __name__ == "__main__":
    main()