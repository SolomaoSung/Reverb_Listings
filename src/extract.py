import pandas as pd
import requests
import os
import dotenv
import argparse
from config import API_URL, PROJECT_ROOT
from pathlib import Path

RAW_DIR = PROJECT_ROOT / 'data' / 'raw'

def collect_page(headers:dict, page:int=1)-> list:
    resp = requests.get(url=API_URL, params={"page":page}, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data['listings']
     
def run(output_dir: Path=RAW_DIR)-> Path:
    dotenv.load_dotenv(PROJECT_ROOT / ".env")
    token = os.getenv("REVERB_TOKEN")

    if not token:
        raise ValueError("Defina REVERB_TOKEN no arquivo .env.")

    headers = {
        "Content-Type": "application/hal+json",
        "Accept": "application/hal+json",
        "Accept-Version": "3.0",
        "Authorization": f"Bearer {token}",
    }

    listings = []
    page = 1

    while True:
        try:
            listing = collect_page(headers=headers, page=page)
        except requests.exceptions.RequestException as err:
            print(f"Failed to extract page {page}: {err}")
            break 

        if not listing:
            break
        listings.extend(listing)
        print(f"Page {page} collected.")
        page += 1

    if not listings:
        print("No listing extracted.")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "listings.parquet"
    df = pd.DataFrame(listings)
    df.to_parquet(output_path, index=False)
    print(f"Parquet file with {len(df)} rows created at {output_path}.")
    return output_path

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=RAW_DIR, type=Path, help="Path to the raw data")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    raise SystemExit(run(args.output))

