import duckdb
import os

def export_to_parquet():

    os.makedirs("../exports", exist_ok=True)

    tables = [
        "tb_category",
        "tb_listings_category",
        "tb_make",
        "tb_shop",
        "tb_condition",
        "tb_shipping_region",
        "tb_shipping_rates_region",
        "tb_listings"
    ]

    with duckdb.connect("../data/reverb.duckdb") as con:

        for table in tables:
            con.execute(f"""
                COPY {table}
                TO '../exports/{table}.parquet'
                (FORMAT PARQUET)
            """)

            print(f"{table} exportada.")