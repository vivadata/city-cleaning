SELECT
    modele AS id,
    type AS type_declaration,
    soustype AS sous_type_declaration ,
    code_postal AS code_postal,
    datedecl AS date_declaration,
    INTERVENANT AS intervenant,
    geo_point_2d AS coordonnees
FROM {{source('city_cleaning', 'dmr')}}