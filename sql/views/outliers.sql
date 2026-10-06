CREATE OR REPLACE VIEW vw_listings_analysis AS(
WITH tb_iqr AS(
SELECT  category,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) AS q3,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) -
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price)
        AS iqr
FROM listings
GROUP BY 1
),

tb_bound AS(
SELECT  category,
        q1 - (1.5 * iqr) AS lower_bound,
        q3 + (1.5 * iqr) AS upper_bound,
        iqr
FROM tb_iqr
)

SELECT  t1.*,
        ROUND(t2.upper_bound::numeric, 2) AS upper_bound,
        CASE WHEN t1.price >= t2.upper_bound THEN 1 ELSE 0
        END AS is_outlier
FROM listings t1
JOIN tb_bound t2
ON t1.category = t2.category
)