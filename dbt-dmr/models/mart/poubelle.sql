WITH
 colonne_verre AS (
    SELECT * FROM {{ref('stg_colonne_verre')}}
),

composteur AS (
    SELECT * FROM {{ref('stg_composteur')}}
),

recyclerie AS (
    SELECT * FROM {{ref('stg_recyclerie')}}
),

textile AS (
    SELECT * FROM {{ref('stg_textile')}}
),

trilib AS (
    SELECT * FROM {{ref('stg_trilib')}}
),

joined AS (
    SELECT
        colonne_verre.coordonnees_poubelle AS geo_verre, 
        composteur.coordonnees_poubelle AS geo_composteur, 
        recyclerie.coordonnees_poubelle AS geo_recyclerie,
        textile.coordonnees_poubelle AS geo_textile,
        trilib.coordonnees_poubelle AS geo_trilib
        
        FROM colonne_verre
        
        JOIN composteur 
        
        ON colonne_verre.code_postal = composteur.code_postal

        JOIN recyclerie 
        
        ON composteur.code_postal = recyclerie.code_postal

        JOIN textile 
        
        ON recyclerie.code_postal = textile.code_postal

        JOIN trilib 
        
        ON textile.code_postal = trilib.code_postal 
)

SELECT * FROM joined