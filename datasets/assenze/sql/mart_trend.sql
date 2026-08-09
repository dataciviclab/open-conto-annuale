-- mart_trend — Assenze per comparto: trend multi-anno
--
-- Legge TUTTI gli anni dal clean via `mart.tables[].years` (view clean_input
-- bindata dal toolkit sui parquet multi-anno). 1 riga = 1 comparto.
-- Risponde: quanto è cresciuto/diminuito assenze per comparto?

with per_anno as (
    select
        anno,
        codi_comparto,
        desc_comparto,
        sum(assenze_uomini) as tot_assenze_uomini,
        sum(assenze_donne) as tot_assenze_donne,
        sum(coalesce(assenze_uomini,0) + coalesce(assenze_donne,0)) as tot_assenze,
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
    arg_min(tot_assenze, anno) as tot_assenze_first,
    arg_max(tot_assenze, anno) as tot_assenze_last,
    arg_max(tot_assenze, anno) - arg_min(tot_assenze, anno) as delta_tot_assenze,
    round(
        100.0 * (arg_max(tot_assenze, anno) - arg_min(tot_assenze, anno))
        / nullif(arg_min(tot_assenze, anno), 0),
        1
    ) as variazione_pct,
    round(
        100.0 * (power(arg_max(tot_assenze, anno)::double / nullif(arg_min(tot_assenze, anno), 0),
                 1.0 / nullif(max(anno) - min(anno), 0)) - 1),
        1
    ) as cagr_pct
from per_anno
group by 1, 2;
