-- mart_trend — Passaggi per comparto: trend multi-anno
--
-- Legge TUTTI gli anni dal clean via `mart.tables[].years` (view clean_input
-- bindata dal toolkit sui parquet multi-anno). 1 riga = 1 comparto.
-- Risponde: quanto è cresciuto/diminuito passaggi di qualifica per comparto?

with per_anno as (
    select
        anno,
        codi_comparto,
        desc_comparto,
        sum(numero_passaggi) as tot_passaggi,
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
    arg_min(tot_passaggi, anno) as tot_passaggi_first,
    arg_max(tot_passaggi, anno) as tot_passaggi_last,
    arg_max(tot_passaggi, anno) - arg_min(tot_passaggi, anno) as delta_tot_passaggi,
    round(
        100.0 * (arg_max(tot_passaggi, anno) - arg_min(tot_passaggi, anno))
        / nullif(arg_min(tot_passaggi, anno), 0),
        1
    ) as variazione_pct,
    round(
        100.0 * (power(arg_max(tot_passaggi, anno)::double / nullif(arg_min(tot_passaggi, anno), 0),
                 1.0 / nullif(max(anno) - min(anno), 0)) - 1),
        1
    ) as cagr_pct
from per_anno
group by 1, 2;
