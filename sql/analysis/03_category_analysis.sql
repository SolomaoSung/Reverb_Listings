SELECT  category,
        COUNT(*) AS total_listings_cat,
        AVG(price) AS avg_price_cat,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) AS median_price_cat,
        ROUND((100 * (AVG(price) - PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price)) /
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price))::numeric,2) AS avg_above_median_pct,
        MAX(price) AS max_price_cat,
        MIN(price) AS min_price_cat,
        ROUND(100. * COUNT(*) / SUM(COUNT (*)) OVER(), 2) AS cat_share
FROM listings
GROUP BY category
ORDER BY 2 DESC

/*
Key findings:
- Effects and Pedals dominate the ranking with the highest number of listings, 
  with Electric Guitars coming in second.
- Acoustics Guitar has the highest average price, Electric Guitars coming in second.
- Keyboards and Synths exhibit a significant disparity between the average and median prices.
  This likely reflects the wide variation in pricing across different models.
*/