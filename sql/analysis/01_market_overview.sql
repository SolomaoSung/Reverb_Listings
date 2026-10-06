SELECT  COUNT(DISTINCT id) AS total_listings,
        COUNT(DISTINCT make) AS total_brands,
        COUNT(DISTINCT category) AS total_categories,
        AVG(price) AS avg_price,
        PERCENTILE_CONT(0.5)
        WITHIN GROUP(ORDER BY price) AS median_price,
        MAX(price) AS highest_valor,
        MIN(price) AS lowest_valor
FROM listings


