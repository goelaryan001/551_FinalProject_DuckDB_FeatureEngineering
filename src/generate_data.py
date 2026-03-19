from pathlib import Path
import numpy as np
import pandas as pd


def generate_transactions(n_rows: int = 100_000, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)

    start_time = pd.Timestamp("2023-01-01")

    df = pd.DataFrame({
        "transaction_id": np.arange(1, n_rows + 1),
        "user_id": np.random.randint(1, 5001, size=n_rows),
        "merchant_id": np.random.randint(1, 501, size=n_rows),
        "amount": np.round(np.random.uniform(5, 500, size=n_rows), 2),
        "category": np.random.choice(
            ["food", "tech", "clothing", "travel", "entertainment", "utilities"],
            size=n_rows
        ),
        "payment_method": np.random.choice(
            ["credit_card", "debit_card", "paypal", "apple_pay", "google_pay"],
            size=n_rows
        ),
        "city": np.random.choice(
            ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
            size=n_rows
        ),
        "is_fraud": np.random.choice([0, 1], size=n_rows, p=[0.98, 0.02]),
        "transaction_time": [
            start_time + pd.Timedelta(minutes=int(x))
            for x in np.random.randint(0, 60 * 24 * 365, size=n_rows)
        ]
    })

    return df


def main():
    project_root = Path(__file__).resolve().parents[1]
    raw_data_dir = project_root / "raw_data"
    raw_data_dir.mkdir(exist_ok=True)

    df = generate_transactions()

    output_path = raw_data_dir / "transactions.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved {len(df)} rows to {output_path}")


if __name__ == "__main__":
    main()