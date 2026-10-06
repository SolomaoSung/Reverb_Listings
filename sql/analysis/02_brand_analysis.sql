WITH tb_brand AS(
SELECT  make AS brand,
        COUNT(*) AS total_listings_brand,
        AVG(price) AS avg_price_brand,
        PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY price) AS median_price_brand,
        MAX(price) AS max_price_brand,
        MIN(price) AS min_price_brand,
        100. * COUNT(*) / SUM(COUNT(*)) OVER() AS market_share
FROM listings
GROUP BY 1
)

SELECT  brand,
        total_listings_brand,
        avg_price_brand,
        median_price_brand,
        max_price_brand,
        min_price_brand,
        ROUND(market_share, 2),
        ROUND(SUM(market_share) OVER(ORDER BY total_listings_brand DESC), 2) AS cumulative_market_share
FROM tb_brand

/*
Key findings:
- Fender and Gibson dominate the listings, with Fender significantly ahead of the rest.
  Fender’s lead reflects its status as the most popular guitar brand.
- Gibson’s average listing price ranks highest among the top five brands.
  This likely reflects its positioning as a premium brand.
*/