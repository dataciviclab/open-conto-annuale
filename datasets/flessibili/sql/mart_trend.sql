-- mart_trend — Flessibili per comparto: trend multi-anno
--
-- Legge TUTTI gli anni dal clean via `mart.tables[].years` (view clean_input
-- bindata dal toolkit sui parquet multi-anno). 1 riga = 1 comparto.
-- Risponde: quanto è cresciuto/diminuito lavoratori flessibili per comparto?

with per_anno as (
    select
        anno,
        codi_comparto,
        desc_comparto,
        sum(coalesce(td_u,0)+coalesce(td_d,0)) as tot_td,
        sum(coalesce(fl_u,0)+coalesce(fl_d,0)) as tot_fl,
        sum(coalesce(int_u,0)+coalesce(int_d,0)) as tot_int,
        sum(coalesce(lsu_u,0)+coalesce(lsu_d,0)) as tot_lsu,
        sum(coalesce(td_u,0)+coalesce(td_d,0)+coalesce(fl_u,0)+coalesce(fl_d,0)+coalesce(int_u,0)+coalesce(int_d,0)+coalesce(lsu_u,0)+coalesce(lsu_d,0)) as tot_flessibili,
        count(distinct istituzione) as enti
    from clean_input
    where codi_comparto is not null
    group by 1, 2, 3
)
select
    codi_comparto,
    desc_comparto,
    min(anno) as first_year,
    max(anno) as last_year,
    arg_min(tot_flessibili, anno) as tot_flessibili_first,
    arg_max(tot_flessibili, anno) as tot_flessibili_last,
    arg_max(tot_flessibili, anno) - arg_min(tot_flessibili, anno) as delta_tot_flessibili,
    round(
        100.0 * (arg_max(tot_flessibili, anno) - arg_min(tot_flessibili, anno))
        / nullif(arg_min(tot_flessibili, anno), 0),
        1
    ) as variazione_pct,
    round(
        100.0 * (power(arg_max(tot_flessibili, anno)::double / nullif(arg_min(tot_flessibili, anno), 0),
                 1.0 / nullif(max(anno) - min(anno), 0)) - 1),
        1
    ) as cagr_pct
from per_anno
group by 1, 2;
