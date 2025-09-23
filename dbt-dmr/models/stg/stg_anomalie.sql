SELECT
    `ID DECLARATION` AS id,
    `TYPE DECLARATION` AS type_declaration,
    `SOUS TYPE DECLARATION` AS sous_type_declaration ,
    `CODE POSTAL` AS code_postal,
    `DATE DECLARATION` AS date_declaration,
    INTERVENANT AS intervenant,
    geo_point_2d AS coordonnees
FROM {{source('city_cleaning', 'dmr')}}