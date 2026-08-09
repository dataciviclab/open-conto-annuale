-- mart_sintesi — Comandati per comparto e anno
--
-- Grano: comparto × anno. Risponde: personale comandato/fuori ruolo per comparto.
-- 1 riga = 1 (anno, comparto).

select
    anno,
    codi_comparto,
    desc_comparto,
    sum(comand_dist_u + fuori_ruolo_u) as tot_comand_u,
    sum(comand_dist_d + fuori_ruolo_d) as tot_comand_d,
    sum(coalesce(comand_dist_u,0)+coalesce(comand_dist_d,0)+coalesce(fuori_ruolo_u,0)+coalesce(fuori_ruolo_d,0)) as tot_comandati,
    round(100.0 * sum(coalesce(comand_dist_d,0)+coalesce(fuori_ruolo_d,0)) / nullif(sum(coalesce(comand_dist_u,0)+coalesce(comand_dist_d,0)+coalesce(fuori_ruolo_u,0)+coalesce(fuori_ruolo_d,0)), 0), 1) as pct_donne,
    count(distinct istituzione) as enti
from clean_input
where codi_comparto is not null
group by 1, 2, 3;
