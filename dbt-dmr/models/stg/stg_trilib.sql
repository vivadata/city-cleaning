SELECT
code_postal,
coordonnees_geo_wgs84 AS coordonnees_poubelle
FROM {{ source('city_cleaning', 'trilib') }}