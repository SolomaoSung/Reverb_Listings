# %%
import pandas as pd
import requests
import dotenv
import os
import argparse
from datetime import datetime 

dotenv.load_dotenv()
REVERB_TOKEN = os.getenv("REVERB_TOKEN")
# %%

class Collector:
    
    def __init__(self, token, output_folder="../data/raw"):

        self.token = token
        self.headers = {
        "Content-Type": "application/hal+json", 
        "Accept": "application/hal+json",     
        "Accept-Version": "3.0", 
        "Authorization": f"Bearer {self.token}"
        }

        self.output_folder = output_folder
        
    def extract_listing(self, page:int=1)->list:

        try:
            resp = requests.get(url=f"https://api.reverb.com/api/listings?page={page}", headers=self.headers)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as err:
            print(err)
            return []
    
        listing = data["listings"]
        return listing

    def extract_batch(self, count:int, max_pages:int=100)->list:

        all_listings = []

        start_page = count * max_pages + 1

        for page in range(start_page, max_pages + start_page):
            listing = self.extract_listing(page)
            if not listing:
                break
            all_listings.extend(listing)
            print(f"Página(s) {page}")
        
        return all_listings
        
    def save_batches(self, listings:list, count:int):

        os.makedirs(self.output_folder, exist_ok=True)

        df = pd.DataFrame(listings)
        df.to_parquet(f"{self.output_folder}/{datetime.now().date()}_batch_{count:02}.parquet", index=False)

    def extract_batches(self, n_batches:int=10, count:int=0):

        for _ in range(0, n_batches):
            all_listings = self.extract_batch(count)
            if not all_listings:
                break
            self.save_batches(all_listings, count)
            count += 1
    
# %%
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--n_batches", type=int, default=10)

    args = parser.parse_args()

    collect = Collector(REVERB_TOKEN)
    collect.extract_batches(n_batches=args.n_batches)
# %%
