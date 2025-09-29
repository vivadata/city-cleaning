from google.cloud import bigquery
import pandas as pd

"""Load data from a BigQuery table into a pandas DataFrame."""

def load_bigquery_table(
    project_id: str,
    dataset_id: str,
    table_id: str,
    max_results: int | None = None
) -> pd.DataFrame:
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    query = f"SELECT * FROM {table_ref}"
    if max_results is not None:
        query += f" LIMIT {max_results}"
    df = client.query(query).to_dataframe()
    return df

def load_local_csv(
    csv_path: str,
    sep: str = ",",
    encoding: str = "utf-8"
) -> pd.DataFrame:
    return pd.read_csv(csv_path, sep=sep, encoding=encoding)

def save_dataframe_to_csv(df: pd.DataFrame, csv_path: str) -> None:
    """Save a pandas DataFrame to a CSV file without the index."""
    df.to_csv(csv_path, index=False)

if __name__ == "__main__":
    # Fetch all rows from BigQuery (no LIMIT) and save to CSV
    df = load_bigquery_table(
        project_id="rue-de-paris-472314",
        dataset_id="datasets",
        table_id="dmr",
        max_results=None  # fetch all rows
    )
    print(f"Fetched {len(df)} rows from BigQuery.")

    # Save to CSV
    output_csv_path = "bigquery_export.csv"
    save_dataframe_to_csv(df, output_csv_path)
    print(f"Data saved to {output_csv_path}.")