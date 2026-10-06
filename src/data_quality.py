# %%
from dataclasses import asdict, dataclass
import pandas as pd
from config import PROJECT_ROOT
from pathlib import Path
import json
import argparse

DEFAULT_INPUT = PROJECT_ROOT / "data" / "processed" / "processed_listings.parquet"
DEFAULT_OUTPUT = PROJECT_ROOT / "reports" / "data_quality.json"

# %%
@dataclass
class Check:
    name: str
    status: str
    details: str

def evaluate(df: pd.DataFrame)-> list:
    checks = []

    def add(name:str, passed:bool, details:str)-> None:
        checks.append(Check(name, "PASS" if passed else "FAIL", details)) 

    add("null_value", int(df.isna().sum().sum() == 0), f"null_cells={int(df.isna().sum().sum())}")
    add("duplicated_rows", int(df.duplicated().sum() == 0), f"duplicates={int(df.duplicated().sum())}")
    add("unique_id", df["id"].is_unique and df["id"].notna().all(), f"unique_id={df['id'].nunique()}")
    return checks

def run(input_path:Path=DEFAULT_INPUT, output_path:Path=DEFAULT_OUTPUT):
    df = pd.read_parquet(input_path)
    checks = evaluate(df)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps([asdict(check) for check in checks], indent=2), encoding="utf-8")

    for check in checks:
        print(f"Name: {check.name}, status: {check.status}, details: {check.details}")

    return 1 if any(check.status == 'FAIL' for check in checks) else 0

def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parse.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parse.parse_args()

if __name__ == "__main__":
    args = parse_args()
    raise SystemExit(run(args.input, args.output))
# %%

