# %%
from collect import Collector
from send import Sender
import dotenv
import os

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

def main():
    # Camada Bronze
    process_raw_data()

if __name__ == "__main__":
    main()

# %%
