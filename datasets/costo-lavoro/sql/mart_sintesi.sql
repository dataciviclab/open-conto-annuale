-- mart_sintesi — Costo del lavoro per comparto e anno
--
-- Grano: comparto × anno. Risponde: quanto costa il personale per comparto.
-- 1 riga = 1 (anno, comparto).

select
    anno,
    codi_comparto,
    desc_comparto,
    sum(totale_spesa) as tot_spesa,
    round(sum(totale_spesa) / 1e6, 1) as tot_spesa_milioni,
    count(distinct istituzione) as enti
from clean_input
where codi_comparto is not null
group by 1, 2, 3;
