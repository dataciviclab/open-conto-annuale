-- mart_trend — Personale per comparto: trend multi-anno
--
-- Legge TUTTI gli anni dal clean via `mart.tables[].years` (view clean_input
-- bindata dal toolkit sui parquet multi-anno). 1 riga = 1 comparto.
-- Risponde: quanto è cresciuto/diminuito il personale per comparto?

with per_anno as (
    select
        anno,
        codi_comparto,
        desc_comparto,
        sum(uomini) as tot_uomini,
        sum(donne) as tot_donne,
        sum(uomini + donne) as tot_dipendenti,
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
    arg_min(tot_dipendenti, anno) as dipendenti_first,
    arg_max(tot_dipendenti, anno) as dipendenti_last,
    arg_max(tot_dipendenti, anno) - arg_min(tot_dipendenti, anno) as delta_dipendenti,
    round(
        100.0 * (arg_max(tot_dipendenti, anno) - arg_min(tot_dipendenti, anno))
        / nullif(arg_min(tot_dipendenti, anno), 0),
        1
    ) as variazione_pct,
    round(
        100.0 * (power(arg_max(tot_dipendenti, anno)::double / nullif(arg_min(tot_dipendenti, anno), 0),
                 1.0 / nullif(max(anno) - min(anno), 0)) - 1),
        1
    ) as cagr_pct
from per_anno
group by 1, 2;
