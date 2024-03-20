-- 2-best_band_ever.sql
-- Task: Rank country origins of bands by the number of (non-unique) fans

-- Rank country origins of bands by the number of (non-unique) fans
SELECT origin, COUNT(fans.name) AS nb_fans
FROM bands
JOIN fans ON bands.name = fans.band_name
GROUP BY origin
ORDER BY nb_fans DESC;
