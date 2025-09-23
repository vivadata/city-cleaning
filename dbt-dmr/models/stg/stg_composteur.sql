SELECT
`Arrondissement de l'emplacement` AS code_postal,
geo_point_2d AS coordonnees_poubelle
FROM {{ source('city_cleaning', 'composteur') }}