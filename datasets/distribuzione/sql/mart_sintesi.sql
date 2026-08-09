-- mart_sintesi — Distribuzione per comparto e anno
--
-- Grano: comparto × anno. Risponde: distribuzione per comparto.
-- 1 riga = 1 (anno, comparto).

select
    anno,
    codi_comparto,
    desc_comparto,
    sum(uomini) as tot_uomini,
    sum(donne) as tot_donne,
    sum(uomini + donne) as tot_dipendenti,
    round(100.0 * sum(donne) / nullif(sum(uomini + donne), 0), 1) as pct_donne,
    count(distinct istituzione) as enti
from clean_input
where codi_comparto is not null
group by 1, 2, 3;
