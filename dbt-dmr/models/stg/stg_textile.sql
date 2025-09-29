SELECT
code_postal,
coordonnees_geo AS coordonnees_poubelle
FROM {{ source('city_cleaning', 'textile') }}