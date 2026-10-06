WITH tb_brand_category AS(
SELECT  make AS brand,
        category,
        COUNT(*) AS listings_brand_cat,
        ROUND(AVG(price)::numeric, 2) AS avg_price_brand_cat,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) AS median_price_brand_cat,
        MAX(price) AS max_price_brand_cat,
        MIN(price) AS min_price_brand_cat,
        ROUND(100. * COUNT(*) / SUM(COUNT (*)) OVER(PARTITION BY category), 2) AS brand_cat_share
FROM listings
GROUP BY 1, 2
),

tb_rank AS(
SELECT  ROW_NUMBER() OVER(PARTITION BY category ORDER BY listings_brand_cat DESC) AS brand_rank,
        brand,
        category,
        listings_brand_cat,
        avg_price_brand_cat,
        median_price_brand_cat,
        max_price_brand_cat,
        min_price_brand_cat,
        brand_cat_share
FROM tb_brand_category
)

SELECT * 
from tb_rank
WHERE brand_rank <= 5

/*
- Fender leads in popularity across Accessories, Amps, Bass Guitars, Parts, and Electric Guitars.
  It also appears in fifth position for Acoustic Guitars.
  This reinforces its status as the most dominant brand in the instrument market.
- Acoustic Guitars from Martin and Gibson exhibit significantly higher average prices.
  This reflects their positioning as premium brands.
*/