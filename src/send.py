# %%
import duckdb
import os
import argparse
# %%
class Sender:

    def __init__(self, output_folder:str="../data", raw_folder:str="../data/raw"):
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

        self.raw_folder = raw_folder

    def send_parquet_data(self,
                          file_name:str="reverb.duckdb", 
                          table:str="bronze_listings"):
        with duckdb.connect(
            f"{self.output_folder}/{file_name}"
        ) as con:
                
            con.execute(f"""
                CREATE TABLE IF NOT EXISTS {table} AS
                SELECT *
                FROM read_parquet('{self.raw_folder}/*.parquet')
                LIMIT 0
            """)

            con.execute(f"""
                INSERT INTO {table}
                SELECT * 
                FROM read_parquet('{self.raw_folder}/*.parquet') p
                WHERE NOT EXISTS(
                SELECT 1 
                FROM {table} b
                WHERE p.id = b.id
                )
            """)

            rows = con.execute(f"""
                SELECT COUNT(*) FROM {table}
            """).fetchone()[0]

            print(f"{rows} registros carregados na tabela {table}.")
            return rows
    
    def send_query_data(self, new_table:str, query:str,
                        file_name:str="reverb.duckdb"):
        with duckdb.connect(
            f"{self.output_folder}/{file_name}"
        ) as con:

            try:
                con.execute(f"""
                    CREATE OR REPLACE TABLE {new_table} AS
                    {query}
                """)
            except Exception as err:
                print(f"Erro ao criar {new_table}: {err}")
                return 
            
            rows = con.execute(f"""
                SELECT COUNT(*) FROM {new_table}
            """).fetchone()[0]

            print(f"{rows} registros carregados na tabela {new_table}.")
            return rows
# %%
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--output_folder", type=str, default="../data")
    parser.add_argument("--raw_folder", type=str, default="../data/raw")
    parser.add_argument("--file_name", type=str, default="reverb.duckdb")
    parser.add_argument("--table", type=str, default="bronze_listings")


    args = parser.parse_args()

    send = Sender(args.output_folder, args.raw_folder)
    rows = send.send_parquet_data(args.file_name, args.table)
    print(f"{rows} registrados carregados.")
# %%
