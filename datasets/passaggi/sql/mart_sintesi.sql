-- mart_sintesi — Passaggi per comparto e anno
--
-- Grano: comparto × anno. Risponde: passaggi di qualifica per comparto.
-- 1 riga = 1 (anno, comparto).

select
    anno,
    codi_comparto,
    desc_comparto,
    sum(numero_passaggi) as tot_passaggi,
    count(distinct istituzione) as enti
from clean_input
where codi_comparto is not null
group by 1, 2, 3;
