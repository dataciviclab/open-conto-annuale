-- mart_sintesi — Contrattazione per comparto e anno
--
-- Grano: comparto × anno. Risponde: spesa di contrattazione integrativa per comparto.
-- 1 riga = 1 (anno, comparto).

select
    anno,
    codi_comparto,
    desc_comparto,
    sum(importo) as tot_importo,
    count(distinct istituzione) as enti
from clean_input
where codi_comparto is not null
group by 1, 2, 3;
