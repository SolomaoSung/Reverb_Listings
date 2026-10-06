SELECT  condition,
        COUNT(*) AS listings_condition,
        AVG(price) AS avg_price_condition,
        PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY price) AS median_condition
FROM listings
GROUP BY 1
ORDER BY 3 DESC;

WITH tb_condition AS (
SELECT  make,
        category,
        condition,
        COUNT(*) AS listings,
        ROUND(AVG(price)::numeric, 2) AS avg_price,
        PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY price) AS median_price,
        MAX(price) AS max_price,
        MIN(price) AS min_price
FROM listings
GROUP BY 1,2,3
HAVING COUNT(*) >= 10   
),

tb_comparable AS(
SELECT  make,
        category,
        COUNT(DISTINCT condition) AS total_condition
FROM tb_condition
GROUP BY 1, 2
HAVING COUNT(DISTINCT condition) >= 2
)

SELECT  t1.*,
        t2.total_condition
FROM tb_condition t1
JOIN tb_comparable t2
ON t1.make = t2.make
AND t1.category = t2.category
;

/*
/*
Key findings:
- Listings in Excellent condition dominate the market and, interestingly, show both a higher 
  average price and median price compared to Mint.
- However, Excellent condition also displays a large gap between its average and median prices, 
  indicating that some listings are priced significantly higher than the rest.
- The depreciation curve highlights how condition strongly influences market value, 
  with Poor listings nearly irrelevant in terms of price.
*/





-- WITH tb_groups AS (
--     SELECT
--         make,
--         category,
--         condition,
--         COUNT(*) AS listings
--     FROM listings
--     GROUP BY make, category, condition
-- ),

-- tb_filtered AS(
-- SELECT
--     COUNT(*) FILTER (WHERE listings >= 1) AS groups_1,
--     COUNT(*) FILTER (WHERE listings >= 5) AS groups_5,
--     COUNT(*) FILTER (WHERE listings >= 10) AS groups_10,
--     COUNT(*) FILTER (WHERE listings >= 20) AS groups_20,
--     COUNT(*) FILTER (WHERE listings >= 30) AS groups_30,
--     COUNT(*) FILTER (WHERE listings >= 50) AS groups_50
-- FROM tb_groups
-- )

-- SELECT  '1' AS min_listings,
--         groups_1 AS quantity
-- FROM tb_filtered
-- UNION ALL
-- SELECT  '5' AS min_listings,
--         groups_5 AS quantity
-- FROM tb_filtered
-- UNION ALL
-- SELECT  '10' AS min_listings,
--         groups_10 AS quantity
-- FROM tb_filtered
-- UNION ALL
-- SELECT  '20' AS min_listings,
--         groups_20 AS quantity
-- FROM tb_filtered
-- UNION ALL
-- SELECT  '30' AS min_listings,
--         groups_30 AS quantity
-- FROM tb_filtered
-- UNION ALL
-- SELECT  '50' AS min_listings,
--         groups_50 AS quantity
-- FROM tb_filtered
-- ;
