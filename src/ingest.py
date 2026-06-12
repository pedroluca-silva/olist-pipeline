import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

DB_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DB_URL)

RAW_PATH = "data/raw"

CSV_FILES = [
     "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv"
]

def ingest_csv(filename):
    table_name = filename.replace(".csv", "")
    filepath = os.path.join(RAW_PATH, filename)
    df = pd.read_csv(filepath)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"✔ {table_name} — {len(df)} linhas carregadas")

if __name__ == "__main__":
    print("Iniciando ingestão...")
    for file in CSV_FILES:
        ingest_csv(file)
    print("Ingestão concluída")