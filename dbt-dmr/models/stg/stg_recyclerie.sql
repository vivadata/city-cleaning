SELECT
CODE_POSTAL AS code_postal,
`Coordonnées Géo` AS coordonnees_poubelle
FROM {{ source('city_cleaning', 'recyclerie') }}