import json
import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)

# %%
class Transformer:

    def load_json(self, cols, df):
        for col in cols:
            df[col] = df[col].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
        return df
    
    def extract_from_list(self, cols, df):
        for col in cols:
            df[col] = df[col].apply(lambda x: x[0] 
                                if isinstance(x, (list, np.ndarray)) and len(x) > 0 else None)
        return df
            
    def process_load_extract_list(self, cols, df):
        df = self.load_json(cols, df)
        df = self.extract_from_list(cols, df)
        return df

    def normalize(self, cols, df):
        expanded = []
        for col in cols:
            if col is not None and col in df.columns:
                expanded.append(pd.json_normalize(df[col].apply(lambda x: x if isinstance(x, dict) else {}),
                                                  max_level=1).add_prefix(f"{col}_"))            
        df = df.drop(columns=cols, errors="ignore")
        return pd.concat([df] + expanded,axis=1)    

    def process_data(self, df):

        json_cols = ["shop", "condition", "price", "buyer_price", "state", "shipping", "_links", 
                        "original_price", "ribbon", "sale_ribbon"]

        list_cols = ["categories", "photos"]

        EXPECTED_COLS = ['id','make','model','finish','year','title','created_at','shop_name','description','inventory','has_inventory','offers_enabled','listing_currency','published_at','auction','shop_id','us_outlet','sku','price_guide_id','original_price_description','categories_uuid','categories_full_name','shop_slug','shop_preferred_seller','condition_uuid','condition_display_name','condition_slug','price_tax_included','price_amount','price_amount_cents','price_currency','price_symbol','price_display','buyer_price_tax_included','buyer_price_amount','buyer_price_amount_cents','buyer_price_currency','buyer_price_symbol','buyer_price_display','state_slug','state_description','shipping_free_expedited_shipping','shipping_local','shipping_initial_offer_rate.region_code','shipping_initial_offer_rate.carrier_calculated','shipping_initial_offer_rate.regional','shipping_initial_offer_rate.destination_postal_code_needed','shipping_user_region_rate.region_code','shipping_user_region_rate.carrier_calculated','shipping_user_region_rate.regional','shipping_user_region_rate.destination_postal_code_needed','_links_photo.href','_links_self.href','_links_edit.href','_links_web.href','_links_cart.href','_links_watchlist.href','_links_make_offer.href','_links_make_offer.method','original_price_tax_included','original_price_amount','original_price_amount_cents','original_price_currency','original_price_symbol','original_price_display','ribbon_display','ribbon_reason','sale_ribbon_display','photos__links.large_crop_href','photos__links.small_crop_href','photos__links.full_href','photos__links.thumbnail_href','shipping_rates_region_code','shipping_rates_carrier_calculated','shipping_rates_regional','shipping_rates_destination_postal_code_needed','shipping_rates_rate.amount','shipping_rates_rate.amount_cents','shipping_rates_rate.currency','shipping_rates_rate.symbol','shipping_rates_rate.display','shipping_rates_incremental_rate.amount','shipping_rates_incremental_rate.amount_cents','shipping_rates_incremental_rate.currency','shipping_rates_incremental_rate.symbol','shipping_rates_incremental_rate.display','shipping_initial_offer_rate.rate_original.amount','shipping_initial_offer_rate.rate_original.amount_cents','shipping_initial_offer_rate.rate_original.currency','shipping_initial_offer_rate.rate_original.symbol','shipping_initial_offer_rate.rate_original.display','shipping_initial_offer_rate.rate_display.amount','shipping_initial_offer_rate.rate_display.amount_cents','shipping_initial_offer_rate.rate_display.currency','shipping_initial_offer_rate.rate_display.symbol','shipping_initial_offer_rate.rate_display.display','shipping_user_region_rate.rate_amount','shipping_user_region_rate.rate_amount_cents','shipping_user_region_rate.rate_currency','shipping_user_region_rate.rate_symbol','shipping_user_region_rate.rate_display','shipping_user_region_rate.incremental_rate_amount','shipping_user_region_rate.incremental_rate_amount_cents','shipping_user_region_rate.incremental_rate_currency','shipping_user_region_rate.incremental_rate_symbol','shipping_user_region_rate.incremental_rate_display']
        
        print("Antes do process_load_extract_list")
        df = self.process_load_extract_list(list_cols, df)
        print("Depois do process_load_extract_list")
        df = self.load_json(json_cols, df)
        print("Depois do load_json")

        df = self.normalize(list_cols + json_cols, df)

        print("Depois do primeiro normalize")
        to_normalize = ["photos__links.large_crop",
        "photos__links.small_crop",
        "photos__links.full",
        "photos__links.thumbnail",
        "shipping_rates",
        "shipping_initial_offer_rate.rate",
        "shipping_user_region_rate.rate",
        "shipping_user_region_rate.incremental_rate"]

        if "shipping_rates" in df.columns:
            print("Antes explode")
            df = df.explode("shipping_rates").reset_index(drop=True)
            print("Antes segundo normalize")
            df = self.normalize(to_normalize, df)
            print("Depois segundo normalize")
        for col in EXPECTED_COLS:
            if col not in df.columns:
                df[col] = None

        return df