# %%
queries = {
    "tb_category": """
        SELECT ROW_NUMBER() OVER(ORDER BY category_name) AS category_id, category_name
        FROM (
            SELECT DISTINCT UNNEST(SPLIT(categories_full_name, '/')) AS category_name
            FROM silver_listings
        )
    """,

    "tb_listings_category": """
        WITH listings_category AS (
            SELECT DISTINCT id AS listings_id,
                   UNNEST(SPLIT(categories_full_name, '/')) AS category_name
            FROM silver_listings
        )
        SELECT ROW_NUMBER() OVER() AS listings_category_id,
               t2.listings_id,
               t1.category_id
        FROM tb_category t1
        JOIN listings_category t2
          ON t1.category_name = t2.category_name
    """,

    "tb_make": """
        SELECT ROW_NUMBER() OVER(ORDER BY make_name) AS make_id, make_name
        FROM (
            SELECT DISTINCT make AS make_name
            FROM silver_listings
        )
    """,

    "tb_shop": """
        SELECT DISTINCT shop_id, shop_name, shop_slug, shop_preferred_seller
        FROM silver_listings
    """,

    "tb_condition": """
        SELECT ROW_NUMBER() OVER(ORDER BY condition_name) AS condition_id, condition_name
        FROM (
            SELECT DISTINCT condition_display_name AS condition_name
            FROM silver_listings
        )
    """,

    "tb_shipping_region": """
        SELECT ROW_NUMBER() OVER(ORDER BY shipping_region) AS shipping_region_id,
               shipping_region
        FROM (
            SELECT DISTINCT shipping_rates_region_code AS shipping_region
            FROM silver_listings
        )
    """,

    "tb_shipping_rates_region": """
        SELECT ROW_NUMBER() OVER(ORDER BY id, shipping_rates_region_code) AS shipping_rate_id,
               t1.id AS listings_id,
               t2.shipping_region,
               t1."shipping_initial_offer_rate.rate_original.amount",
               t1."shipping_initial_offer_rate.rate_original.amount_cents",
               t1."shipping_initial_offer_rate.rate_original.currency",
               t1."shipping_initial_offer_rate.rate_original.symbol",
               t1."shipping_initial_offer_rate.rate_original.display",
               t1."shipping_initial_offer_rate.rate_display.amount",
               t1."shipping_initial_offer_rate.rate_display.amount_cents",
               t1."shipping_initial_offer_rate.rate_display.currency",
               t1."shipping_initial_offer_rate.rate_display.symbol",
               t1."shipping_initial_offer_rate.rate_display.display",
               t1."shipping_user_region_rate.rate_amount",
               t1."shipping_user_region_rate.rate_amount_cents",
               t1."shipping_user_region_rate.rate_currency",
               t1."shipping_user_region_rate.rate_symbol",
               t1."shipping_user_region_rate.rate_display",
               t1."shipping_user_region_rate.incremental_rate_amount",
               t1."shipping_user_region_rate.incremental_rate_amount_cents",
               t1."shipping_user_region_rate.incremental_rate_currency",
               t1."shipping_user_region_rate.incremental_rate_symbol",
               t1."shipping_user_region_rate.incremental_rate_display",
               t1."shipping_rates_destination_postal_code_needed",
               t1."shipping_rates_rate.amount",
               t1."shipping_rates_rate.amount_cents",
               t1."shipping_rates_rate.currency",
               t1."shipping_rates_rate.symbol",
               t1."shipping_rates_rate.display",
               t1."shipping_rates_incremental_rate.amount",
               t1."shipping_rates_incremental_rate.amount_cents",
               t1."shipping_rates_incremental_rate.currency",
               t1."shipping_rates_incremental_rate.symbol",
               t1."shipping_rates_incremental_rate.display"
        FROM silver_listings t1
        LEFT JOIN tb_shipping_region t2
          ON t1.shipping_rates_region_code = t2.shipping_region
        WHERE t1.shipping_rates_region_code IS NOT NULL
    """,

    "tb_listings": """
        SELECT DISTINCT t1.id AS listings_id,
            t3.make_id,
            t1.model,
            t1.finish,
            t1.year,
            t1.title,
            t1.created_at,
            t1.description,
            t1.inventory,
            t1.has_inventory,
            t1.offers_enabled,
            t1.listing_currency,
            t1.published_at,
            t1.auction,
            t1.shop_id,
            t1.us_outlet,
            t1.sku,
            t1.price_guide_id,
            t1.original_price_description,
            t2.condition_id,
            t1.price_tax_included,
            t1.price_amount,
            t1.price_amount_cents,
            t1.price_currency,
            t1.price_symbol,
            t1.price_display,
            t1.buyer_price_tax_included,
            t1.buyer_price_amount,
            t1.buyer_price_amount_cents,
            t1.buyer_price_currency,
            t1.buyer_price_symbol,
            t1.buyer_price_display,
            t1.state_slug,
            t1.state_description,
            t1.shipping_free_expedited_shipping,
            t1.shipping_local,
            t1.original_price_tax_included,
            t1.original_price_amount,
            t1.original_price_amount_cents,
            t1.original_price_currency,
            t1.original_price_symbol,
            t1.original_price_display,
            t1.ribbon_display,
            t1.ribbon_reason,
            t1.sale_ribbon_display
        FROM silver_listings t1
        LEFT JOIN tb_condition t2
          ON t1.condition_display_name = t2.condition_name
        LEFT JOIN tb_make t3
          ON t1.make = t3.make_name
    """
}
# %%
import duckdb

con = duckdb.connect("../data/reverb.duckdb")

con.execute("""SELECT DISTINCT t1.id AS listings_id,
            t3.make_id,
            t1.model,
            t1.finish,
            t1.year,
            t1.title,
            t1.created_at,
            t1.description,
            t1.inventory,
            t1.has_inventory,
            t1.offers_enabled,
            t1.listing_currency,
            t1.published_at,
            t1.auction,
            t1.shop_id,
            t1.us_outlet,
            t1.sku,
            t1.price_guide_id,
            t1.original_price_description,
            t2.condition_id,
            t1.price_tax_included,
            t1.price_amount,
            t1.price_amount_cents,
            t1.price_currency,
            t1.price_symbol,
            t1.price_display,
            t1.buyer_price_tax_included,
            t1.buyer_price_amount,
            t1.buyer_price_amount_cents,
            t1.buyer_price_currency,
            t1.buyer_price_symbol,
            t1.buyer_price_display,
            t1.state_slug,
            t1.state_description,
            t1.shipping_free_expedited_shipping,
            t1.shipping_local,
            t1.original_price_tax_included,
            t1.original_price_amount,
            t1.original_price_amount_cents,
            t1.original_price_currency,
            t1.original_price_symbol,
            t1.original_price_display,
            t1.ribbon_display,
            t1.ribbon_reason,
            t1.sale_ribbon_display
        FROM silver_listings t1
        LEFT JOIN tb_condition t2
          ON t1.condition_display_name = t2.condition_name
        LEFT JOIN tb_make t3
          ON t1.make = t3.make_name""").fetchdf()


# %%
