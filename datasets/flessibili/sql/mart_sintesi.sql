-- mart_sintesi — Flessibili per comparto e anno
--
-- Grano: comparto × anno. Risponde: lavoratori flessibili per comparto.
-- 1 riga = 1 (anno, comparto).

select
    anno,
    codi_comparto,
    desc_comparto,
    sum(coalesce(td_u,0)+coalesce(td_d,0)) as tot_td,
    sum(coalesce(fl_u,0)+coalesce(fl_d,0)) as tot_fl,
    sum(coalesce(int_u,0)+coalesce(int_d,0)) as tot_int,
    sum(coalesce(lsu_u,0)+coalesce(lsu_d,0)) as tot_lsu,
    sum(coalesce(td_u,0)+coalesce(td_d,0)+coalesce(fl_u,0)+coalesce(fl_d,0)+coalesce(int_u,0)+coalesce(int_d,0)+coalesce(lsu_u,0)+coalesce(lsu_d,0)) as tot_flessibili,
    round(100.0 * sum(coalesce(td_d,0)+coalesce(fl_d,0)+coalesce(int_d,0)+coalesce(lsu_d,0)) / nullif(sum(coalesce(td_u,0)+coalesce(td_d,0)+coalesce(fl_u,0)+coalesce(fl_d,0)+coalesce(int_u,0)+coalesce(int_d,0)+coalesce(lsu_u,0)+coalesce(lsu_d,0)), 0), 1) as pct_donne,
    count(distinct istituzione) as enti
from clean_input
where codi_comparto is not null
group by 1, 2, 3;
