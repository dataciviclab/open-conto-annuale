-- mart_sintesi — Retribuzione media per comparto e anno
--
-- Grano: comparto × anno. Risponde: retribuzione media per comparto.
-- 1 riga = 1 (anno, comparto).

select
    anno,
    codi_comparto,
    desc_comparto,
    avg(stipendio) as avg_stipendio,
    avg(tredicesima) as avg_tredicesima,
    avg(straordinario) as avg_straordinario,
    avg(indennita_fisse) as avg_indennita,
    avg(altre_accessorie) as avg_accessorie,
    count(distinct istituzione) as enti
from clean_input
where codi_comparto is not null
group by 1, 2, 3;
