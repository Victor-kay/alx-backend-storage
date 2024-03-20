-- Task: List all bands with Glam rock as their main style, ranked by their longevity

-- List bands with Glam rock as their main style, ranked by their longevity
SELECT band_name, 
       TIMESTAMPDIFF(YEAR, formed, IFNULL(split, '2022-01-01')) AS lifespan
FROM bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
