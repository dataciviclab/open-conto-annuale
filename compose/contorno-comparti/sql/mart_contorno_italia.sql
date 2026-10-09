-- mart_contorno_italia — compose Conto Annuale, aggregato nazionale per anno.
--
-- Ricostruisce l'aggregato Italia dalle stesse sorgenti del compose
-- (personale + costo + occupazione + assenze mart_sintesi multi-anno).
-- Nessun layer clean proprio: compose mart-only.

WITH pers AS (
    SELECT
        anno,
        SUM(tot_dipendenti) AS tot_dipendenti,
        SUM(tot_uomini) AS tot_uomini,
        SUM(tot_donne) AS tot_donne
    FROM read_parquet('{support.personale.path}' || '/*/mart_sintesi.parquet')
    GROUP BY anno
),
costo AS (
    SELECT
        anno,
        SUM(tot_spesa_milioni) AS tot_spesa_milioni
    FROM read_parquet('{support.costo_lavoro.path}' || '/*/mart_sintesi.parquet')
    GROUP BY anno
),
occ AS (
    SELECT
        anno,
        ROUND(100.0 * SUM(tot_part_time) / NULLIF(SUM(tot_dipendenti), 0), 1)
            AS pct_part_time
    FROM read_parquet('{support.occupazione.path}' || '/*/mart_sintesi.parquet')
    GROUP BY anno
),
ass AS (
    SELECT
        anno,
        SUM(tot_assenze) AS tot_assenze
    FROM read_parquet('{support.assenze.path}' || '/*/mart_sintesi.parquet')
    GROUP BY anno
)
SELECT
    p.anno,
    p.tot_dipendenti,
    p.tot_uomini,
    p.tot_donne,
    ROUND(100.0 * p.tot_donne / NULLIF(p.tot_dipendenti, 0), 1) AS pct_donne,
    c.tot_spesa_milioni,
    ROUND(c.tot_spesa_milioni * 1e6 / NULLIF(p.tot_dipendenti, 0) / 1000.0, 1)
        AS spesa_per_dipendente_k,
    o.pct_part_time,
    a.tot_assenze,
    ROUND(a.tot_assenze / NULLIF(p.tot_dipendenti, 0), 1) AS assenze_per_dipendente
FROM pers p
LEFT JOIN costo c ON p.anno = c.anno
LEFT JOIN occ o ON p.anno = o.anno
LEFT JOIN ass a ON p.anno = a.anno
ORDER BY p.anno
