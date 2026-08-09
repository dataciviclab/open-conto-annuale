-- mart_trend — Comandati per comparto: trend multi-anno
--
-- Legge TUTTI gli anni dal clean via `mart.tables[].years` (view clean_input
-- bindata dal toolkit sui parquet multi-anno). 1 riga = 1 comparto.
-- Risponde: quanto è cresciuto/diminuito comandati per comparto?

with per_anno as (
    select
        anno,
        codi_comparto,
        desc_comparto,
        sum(comand_dist_u + fuori_ruolo_u) as tot_comand_u,
        sum(comand_dist_d + fuori_ruolo_d) as tot_comand_d,
        sum(coalesce(comand_dist_u,0)+coalesce(comand_dist_d,0)+coalesce(fuori_ruolo_u,0)+coalesce(fuori_ruolo_d,0)) as tot_comandati,
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
    arg_min(tot_comandati, anno) as tot_comandati_first,
    arg_max(tot_comandati, anno) as tot_comandati_last,
    arg_max(tot_comandati, anno) - arg_min(tot_comandati, anno) as delta_tot_comandati,
    round(
        100.0 * (arg_max(tot_comandati, anno) - arg_min(tot_comandati, anno))
        / nullif(arg_min(tot_comandati, anno), 0),
        1
    ) as variazione_pct,
    round(
        100.0 * (power(arg_max(tot_comandati, anno)::double / nullif(arg_min(tot_comandati, anno), 0),
                 1.0 / nullif(max(anno) - min(anno), 0)) - 1),
        1
    ) as cagr_pct
from per_anno
group by 1, 2;
