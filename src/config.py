from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

API_URL = "https://api.reverb.com/api/listings"

ALL_COLUMNS = ['id', 'make', 'model', 'finish', 'year', 'title', 'created_at', 'shop_name', 'shop', 'description', 
 'condition', 'price', 'buyer_price', 'inventory', 'has_inventory', 'offers_enabled', 'categories', 
 'listing_currency', 'published_at', 'state', 'auction', 'shop_id', 'shipping', 'us_outlet', '_links', 
 'photos', 'sku', 'price_guide_id', 'original_price', 'ribbon', 'original_price_description', 
 'sale_ribbon', 'price_drop']

COLS_TO_USE = ['id', 'make', 'model', 'created_at', 'shop', 'condition', 'price', 'categories']
