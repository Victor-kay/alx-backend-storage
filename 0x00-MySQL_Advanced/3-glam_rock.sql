-- 3-glam_rock.sql
-- Task: List all bands with Glam rock as their main style, ranked by their longevity

-- List all bands with Glam rock as their main style, ranked by their longevity
SELECT band_name, 
       IFNULL(DATEDIFF(2022, formed), 0) - IFNULL(DATEDIFF(2022, split), 0) AS lifespan
FROM bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
