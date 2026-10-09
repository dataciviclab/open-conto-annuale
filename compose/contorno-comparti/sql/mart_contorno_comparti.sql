-- mart_contorno_comparti — compose Conto Annuale
--
-- Grano: (anno, codi_comparto). Spine = personale mart_sintesi.
-- Tutti i join verso gli altri mart_sintesi sono LEFT JOIN (spine personale
-- sempre presente; le altre metriche sono nullable per costruzione).
--
-- Metriche derivate:
--   spesa_per_dipendente  = tot_spesa_milioni / tot_dipendenti (k€/anno)
--   assenze_per_dipendente = tot_assenze / tot_dipendenti
--
-- I support type: file puntano alle directory multi-anno dei mart base;
-- il glob /*/mart_sintesi.parquet copre tutti gli anni presenti in locale.

WITH pers AS (
    SELECT
        anno,
        codi_comparto,
        MAX(desc_comparto) AS desc_comparto,
        MAX(tot_dipendenti) AS tot_dipendenti,
        MAX(pct_donne) AS pct_donne,
        MAX(enti) AS enti_personale
    FROM read_parquet('{support.personale.path}' || '/*/mart_sintesi.parquet')
    GROUP BY anno, codi_comparto
),
costo AS (
    SELECT
        anno,
        codi_comparto,
        tot_spesa_milioni,
        enti AS enti_costo
    FROM read_parquet('{support.costo_lavoro.path}' || '/*/mart_sintesi.parquet')
),
occ AS (
    SELECT
        anno,
        codi_comparto,
        pct_donne AS pct_donne_occ,
        pct_part_time,
        tot_part_time
    FROM read_parquet('{support.occupazione.path}' || '/*/mart_sintesi.parquet')
),
ass AS (
    SELECT
        anno,
        codi_comparto,
        tot_assenze,
        pct_assenze_donne
    FROM read_parquet('{support.assenze.path}' || '/*/mart_sintesi.parquet')
),
retr AS (
    SELECT
        anno,
        codi_comparto,
        avg_stipendio,
        avg_tredicesima,
        avg_straordinario,
        avg_indennita,
        avg_accessorie
    FROM read_parquet('{support.retribuzione_media.path}' || '/*/mart_sintesi.parquet')
),
com AS (
    SELECT
        anno,
        codi_comparto,
        tot_comandati
    FROM read_parquet('{support.comandati.path}' || '/*/mart_sintesi.parquet')
),
contr AS (
    SELECT
        anno,
        codi_comparto,
        tot_importo AS contrattazione_importo
    FROM read_parquet('{support.contrattazione.path}' || '/*/mart_sintesi.parquet')
),
flex AS (
    SELECT
        anno,
        codi_comparto,
        tot_flessibili
    FROM read_parquet('{support.flessibili.path}' || '/*/mart_sintesi.parquet')
),
pass AS (
    SELECT
        anno,
        codi_comparto,
        tot_passaggi
    FROM read_parquet('{support.passaggi.path}' || '/*/mart_sintesi.parquet')
),
tit AS (
    SELECT
        anno,
        codi_comparto,
        tot_dipendenti AS titoli_tot_dip
    FROM read_parquet('{support.titoli_studio.path}' || '/*/mart_sintesi.parquet')
),
anz AS (
    SELECT
        anno,
        codi_comparto,
        tot_dipendenti AS anzianita_tot_dip
    FROM read_parquet('{support.anzianita.path}' || '/*/mart_sintesi.parquet')
),
modf AS (
    SELECT
        anno,
        codi_comparto,
        tot_modalita
    FROM read_parquet('{support.modalita_flessibile.path}' || '/*/mart_sintesi.parquet')
),
dist AS (
    SELECT
        anno,
        codi_comparto,
        tot_uomini AS dist_uomini,
        tot_donne AS dist_donne
    FROM read_parquet('{support.distribuzione.path}' || '/*/mart_sintesi.parquet')
)
SELECT
    p.anno,
    p.codi_comparto,
    p.desc_comparto,
    p.tot_dipendenti,
    p.pct_donne,
    p.enti_personale,
    c.tot_spesa_milioni,
    ROUND(c.tot_spesa_milioni * 1e6 / NULLIF(p.tot_dipendenti, 0) / 1000.0, 1)
        AS spesa_per_dipendente_k,
    o.pct_part_time,
    o.tot_part_time,
    a.tot_assenze,
    ROUND(a.tot_assenze / NULLIF(p.tot_dipendenti, 0), 1)
        AS assenze_per_dipendente,
    a.pct_assenze_donne,
    r.avg_stipendio,
    r.avg_tredicesima,
    r.avg_straordinario,
    r.avg_indennita,
    r.avg_accessorie,
    cm.tot_comandati,
    ct.contrattazione_importo,
    f.tot_flessibili,
    ps.tot_passaggi,
    mo.tot_modalita,
    d.dist_uomini,
    d.dist_donne
FROM pers p
LEFT JOIN costo c
    ON p.anno = c.anno AND p.codi_comparto = c.codi_comparto
LEFT JOIN occ o
    ON p.anno = o.anno AND p.codi_comparto = o.codi_comparto
LEFT JOIN ass a
    ON p.anno = a.anno AND p.codi_comparto = a.codi_comparto
LEFT JOIN retr r
    ON p.anno = r.anno AND p.codi_comparto = r.codi_comparto
LEFT JOIN com cm
    ON p.anno = cm.anno AND p.codi_comparto = cm.codi_comparto
LEFT JOIN contr ct
    ON p.anno = ct.anno AND p.codi_comparto = ct.codi_comparto
LEFT JOIN flex f
    ON p.anno = f.anno AND p.codi_comparto = f.codi_comparto
LEFT JOIN pass ps
    ON p.anno = ps.anno AND p.codi_comparto = ps.codi_comparto
LEFT JOIN modf mo
    ON p.anno = mo.anno AND p.codi_comparto = mo.codi_comparto
LEFT JOIN dist d
    ON p.anno = d.anno AND p.codi_comparto = d.codi_comparto
ORDER BY p.anno, p.codi_comparto
