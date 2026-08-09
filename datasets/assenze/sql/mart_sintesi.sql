-- mart_sintesi — Assenze per comparto e anno
--
-- Grano: comparto × anno. Risponde: assenze per comparto.
-- 1 riga = 1 (anno, comparto).

select
    anno,
    codi_comparto,
    desc_comparto,
    sum(assenze_uomini) as tot_assenze_uomini,
    sum(assenze_donne) as tot_assenze_donne,
    sum(coalesce(assenze_uomini,0) + coalesce(assenze_donne,0)) as tot_assenze,
    round(100.0 * sum(assenze_donne) / nullif(sum(coalesce(assenze_uomini,0) + coalesce(assenze_donne,0)), 0), 1) as pct_assenze_donne,
    count(distinct istituzione) as enti
from clean_input
where codi_comparto is not null
group by 1, 2, 3;
