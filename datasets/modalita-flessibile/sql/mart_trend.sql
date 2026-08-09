-- mart_trend — Modalità flessibile per comparto: trend multi-anno
--
-- Legge TUTTI gli anni dal clean via `mart.tables[].years` (view clean_input
-- bindata dal toolkit sui parquet multi-anno). 1 riga = 1 comparto.
-- Risponde: quanto è cresciuto/diminuito modalità lavoro per comparto?

with per_anno as (
    select
        anno,
        codi_comparto,
        desc_comparto,
        sum(coalesce(tl_u,0)+coalesce(tl_d,0)) as tot_telelavoro,
        sum(coalesce(agile_u,0)+coalesce(agile_d,0)) as tot_agile,
        sum(coalesce(cowork_u,0)+coalesce(cowork_d,0)) as tot_coworking,
        sum(coalesce(turn_u,0)+coalesce(turn_d,0)) as tot_turnazione,
        sum(coalesce(tl_u,0)+coalesce(tl_d,0)+coalesce(agile_u,0)+coalesce(agile_d,0)+coalesce(cowork_u,0)+coalesce(cowork_d,0)+coalesce(turn_u,0)+coalesce(turn_d,0)) as tot_modalita,
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
    arg_min(tot_modalita, anno) as tot_modalita_first,
    arg_max(tot_modalita, anno) as tot_modalita_last,
    arg_max(tot_modalita, anno) - arg_min(tot_modalita, anno) as delta_tot_modalita,
    round(
        100.0 * (arg_max(tot_modalita, anno) - arg_min(tot_modalita, anno))
        / nullif(arg_min(tot_modalita, anno), 0),
        1
    ) as variazione_pct,
    round(
        100.0 * (power(arg_max(tot_modalita, anno)::double / nullif(arg_min(tot_modalita, anno), 0),
                 1.0 / nullif(max(anno) - min(anno), 0)) - 1),
        1
    ) as cagr_pct
from per_anno
group by 1, 2;
