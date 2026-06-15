# %%
from collect import Collector
from send import Sender
from transform import Transformer
import dotenv
import os
import duckdb
import pandas as pd
from models import queries

dotenv.load_dotenv()
REVERB_TOKEN = os.getenv("REVERB_TOKEN")
# %%
def process_raw_data():
    collect = Collector(token=REVERB_TOKEN, output_folder="../data/raw")
    print("Extraindo dados da api...")
    collect.extract_batches()

    send = Sender(output_folder="../data", raw_folder="../data/raw")
    print("Enviando dados...")
    send.send_parquet_data()

def transform_raw_data():
    with duckdb.connect("../data/reverb.duckdb") as con:
        result = con.execute("SELECT * FROM bronze_listings").fetchdf()
        t = Transformer()
        df = t.process_data(result)
        con.register("processed_df", df)
        con.execute("CREATE TABLE IF NOT EXISTS silver_listings AS SELECT *" \
        "FROM processed_df LIMIT 0")
        con.execute("INSERT INTO silver_listings SELECT * FROM processed_df d" \
        " WHERE NOT EXISTS (SELECT 1 FROM silver_listings lp WHERE lp.id = d.id )")

def main():
    # Camada Bronze
    process_raw_data()

    transform_raw_data()

    s = Sender()
    for table, query in queries.items():
        s.send_query_data(table, query)

if __name__ == "__main__":
    main()

# %%
