-- mart_sintesi — Modalità flessibile per comparto e anno
--
-- Grano: comparto × anno. Risponde: modalità di lavoro flessibile per comparto.
-- 1 riga = 1 (anno, comparto).

select
    anno,
    codi_comparto,
    desc_comparto,
    sum(coalesce(tl_u,0)+coalesce(tl_d,0)) as tot_telelavoro,
    sum(coalesce(agile_u,0)+coalesce(agile_d,0)) as tot_agile,
    sum(coalesce(cowork_u,0)+coalesce(cowork_d,0)) as tot_coworking,
    sum(coalesce(turn_u,0)+coalesce(turn_d,0)) as tot_turnazione,
    sum(coalesce(tl_u,0)+coalesce(tl_d,0)+coalesce(agile_u,0)+coalesce(agile_d,0)+coalesce(cowork_u,0)+coalesce(cowork_d,0)+coalesce(turn_u,0)+coalesce(turn_d,0)) as tot_modalita,
    round(100.0 * sum(coalesce(tl_d,0)+coalesce(agile_d,0)+coalesce(cowork_d,0)+coalesce(turn_d,0)) / nullif(sum(coalesce(tl_u,0)+coalesce(tl_d,0)+coalesce(agile_u,0)+coalesce(agile_d,0)+coalesce(cowork_u,0)+coalesce(cowork_d,0)+coalesce(turn_u,0)+coalesce(turn_d,0)), 0), 1) as pct_donne,
    count(distinct istituzione) as enti
from clean_input
where codi_comparto is not null
group by 1, 2, 3;
