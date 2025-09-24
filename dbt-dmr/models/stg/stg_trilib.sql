SELECT
`Code postal` AS code_postal,
`Coordonnees géographiques` AS coordonnees_poubelle
FROM {{ source('city_cleaning', 'trilib') }}