SELECT * FROM {{ref('stg_anomalie')}}
WHERE type_declaration LIKE '%clairage%'