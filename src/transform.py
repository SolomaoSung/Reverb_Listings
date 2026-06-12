# %%
import json
import pandas as pd

pd.set_option("display.max_columns", None)

# %%
class Transformer:

    def load_json(self, cols, df):
        for col in cols:
            df[col] = df[col].apply(lambda x: json.loads(x) if isinstance(x, str) else None)
        return df
    
    def extract_from_list(self, cols, df):
        for col in cols:
            df[col] = df[col].apply(lambda x: x[0] 
                                if isinstance(x, list) and len(x) > 0 else None)
        return df
            
    def process_load_extract_list(self, cols, df):
        df = self.load_json(cols, df)
        df = self.extract_from_list(cols, df)
        return df

    def normalize(self, cols, df):
        expanded = []
        for col in cols:
            expanded.append(pd.json_normalize(df[col],max_level=1).add_prefix(f"{col}_"))
            
        df = df.drop(columns=cols)
        return pd.concat([df] + expanded,axis=1)    

    def process_data(self, df):

        json_cols = ["shop", "condition", "price", "buyer_price", "state", "shipping", "_links", 
                        "original_price", "ribbon", "sale_ribbon"]

        list_cols = ["categories", "photos"]

        df = self.process_load_extract_list(list_cols, df)
        df = self.load_json(json_cols, df)
        df = self.normalize(list_cols + json_cols, df)

        to_normalize = ["photos__links.large_crop",
        "photos__links.small_crop",
        "photos__links.full",
        "photos__links.thumbnail",
        "shipping_rates",
        "shipping_initial_offer_rate.rate",
        "shipping_user_region_rate.rate",
        "shipping_user_region_rate.incremental_rate"]

        df = df.explode("shipping_rates")
        df = self.normalize(to_normalize, df)

        return df
# %%
