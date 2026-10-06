WITH tb_cat AS(
SELECT  category,
        COUNT(*) AS listings,
        AVG(price) AS avg_price,
        PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY price) AS median_price,
        PERCENTILE_CONT(0.25) WITHIN GROUP(ORDER BY price) AS q1_price,
        PERCENTILE_CONT(0.75) WITHIN GROUP(ORDER BY price) AS q3_price,
        PERCENTILE_CONT(0.75) WITHIN GROUP(ORDER BY price) -
        PERCENTILE_CONT(0.25) WITHIN GROUP(ORDER BY price) AS iqr,
        MAX(price) AS max_price,
        MIN(price) AS min_price
FROM listings
GROUP BY category
),

tb_bounds AS(
SELECT  *,
        ROUND((q1_price - 1.5 * iqr)::numeric, 2) AS lower_bound,
        ROUND((q3_price + 1.5 * iqr)::numeric, 2) AS upper_bound
FROM tb_cat
),

tb_listings_bound AS(
SELECT
    l.id,
    l.category,
    l.price,
    b.lower_bound,
    b.upper_bound
FROM listings AS l
JOIN tb_bounds AS b
    ON l.category = b.category
WHERE
    l.price < b.lower_bound
    OR
    l.price > b.upper_bound
)

SELECT  t1.category,
        COUNT(t1.id) AS total_listings,
        COUNT(t2.id) AS outliers,
        ROUND(100. * COUNT(t2.id) / COUNT(t1.id), 2) AS outlier_pct
FROM listings t1
LEFT JOIN tb_listings_bound t2
ON t1.id = t2.id
GROUP BY 1
ORDER BY 2 DESC;

/*
- Keyboards and Synths show the highest outlier percentage, likely driven by the 
  presence of premium, high-priced products within the category.
*/

