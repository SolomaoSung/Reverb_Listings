# %%
import argparse
import pandas as pd
from pathlib import Path
from config import PROJECT_ROOT, COLS_TO_USE

DEFAULT_INPUT = PROJECT_ROOT / "data" / "raw" / "listings.parquet"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "processed" / "processed_listings.parquet"
# %%
def transform(input_path: Path= DEFAULT_INPUT)-> pd.DataFrame:
    df = pd.read_parquet(input_path)
    df = df[COLS_TO_USE].copy()
    df["categories"] = df["categories"].apply(lambda x: x[0] if x is not None and
                                            len(x) > 0 else {})
    def normalize(col: pd.Series) -> pd.DataFrame:
        df_col = pd.json_normalize(col.tolist())
        df_col.index = col.index
        return df_col

    normalized_shop = normalize(df["shop"])
    df.drop(columns="shop", inplace=True)
    df["shop"] = normalized_shop["slug"]
    df["preferred_seller"] = normalized_shop["preferred_seller"]

    normalized_condition = normalize(df["condition"])
    df.drop(columns="condition", inplace=True)
    df["condition"] = normalized_condition["display_name"]

    normalized_price = normalize(df["price"])
    df.drop(columns="price", inplace=True)
    df["price"] = pd.to_numeric(normalized_price["amount"], errors="raise")

    normalized_categories = normalize(df["categories"])
    df.drop(columns="categories", inplace=True)
    df["category"] = (normalized_categories["full_name"].astype("string").str.split("/")
                            .str[0].str.strip())

    cols = ["make", "model"]
    for col in cols:
        df[col] = df[col].astype("string")

    df["created_at"] = pd.to_datetime(df["created_at"], utc=True).dt.normalize()

    df = df.drop_duplicates()

    return df

def run(input_path:Path= DEFAULT_INPUT, output_path:Path= DEFAULT_OUTPUT)-> int:
    df = transform(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)
    return output_path

# %%
def parse_args()-> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default= DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default= DEFAULT_OUTPUT)
    return parser.parse_args()
# %%

if __name__ == "__main__":
    args = parse_args()
    raise SystemExit(run(args.input, args.output))
# %%
