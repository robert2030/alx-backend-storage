-- List all Bands with glam rock as main style
-- Ranked by Longevity

SELECT band_name, IF(split IS NULL, 2022 - formed, split - formed) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', style) > 0
ORDER BY lifespan DESC;
