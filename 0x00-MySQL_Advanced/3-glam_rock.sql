-- Task: List all bands with Glam rock as their main style, ranked by their longevity

-- SELECT query to retrieve bands with Glam rock style and calculate their lifespan
SELECT band_name, 
       FLOOR(DATEDIFF('2022-01-01', formed)/365) - IF(split='-', FLOOR(DATEDIFF('2022-01-01', split)/365), 0) AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
