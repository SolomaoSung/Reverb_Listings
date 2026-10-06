# %% 
from config import PROJECT_ROOT
from pathlib import Path
import sqlalchemy
import argparse
import dotenv
import os
import pandas as pd

VIEW_SQL = PROJECT_ROOT / "sql" / "views" / "outliers.sql"
DEFAULT_INPUT = PROJECT_ROOT / "data" / "processed" / "processed_listings.parquet"

# %%
def run(input_path:Path=DEFAULT_INPUT)-> int:

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1
    
    dotenv.load_dotenv(PROJECT_ROOT / ".env")
    db_url = os.getenv("DB_URL")

    if not db_url:
        print(f"DB_URL not found.")
        return 1
    
    engine = sqlalchemy.create_engine(db_url, pool_pre_ping=True)

    df = pd.read_parquet(input_path)

    view_sql = VIEW_SQL.read_text(encoding="utf-8")

    with engine.begin() as conn:
        df.to_sql("incoming", conn, if_exists="replace", index=False)

        conn.execute(sqlalchemy.text("""
            CREATE TABLE IF NOT EXISTS listings AS
            SELECT *
            FROM incoming
            WHERE FALSE
        """))

        conn.execute(sqlalchemy.text("""
            INSERT INTO listings
            SELECT i.*
            FROM incoming AS i
            WHERE NOT EXISTS (
                SELECT 1
                FROM listings AS l
                WHERE l.id = i.id
            )
        """))

        conn.execute(sqlalchemy.text(view_sql))
    return 0

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    raise SystemExit(run(args.input))