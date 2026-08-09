-- mart_trend — Retribuzione media per comparto: trend multi-anno
--
-- Legge TUTTI gli anni dal clean via `mart.tables[].years` (view clean_input
-- bindata dal toolkit sui parquet multi-anno). 1 riga = 1 comparto.
-- Risponde: quanto è cresciuto/diminuito retribuzione media per comparto?

with per_anno as (
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
    group by 1, 2, 3
)
select
    codi_comparto,
    desc_comparto,
    min(anno) as first_year,
    max(anno) as last_year,
    arg_min(avg_stipendio, anno) as avg_stipendio_first,
    arg_max(avg_stipendio, anno) as avg_stipendio_last,
    arg_max(avg_stipendio, anno) - arg_min(avg_stipendio, anno) as delta_avg_stipendio,
    round(
        100.0 * (arg_max(avg_stipendio, anno) - arg_min(avg_stipendio, anno))
        / nullif(arg_min(avg_stipendio, anno), 0),
        1
    ) as variazione_pct,
    round(
        100.0 * (power(arg_max(avg_stipendio, anno)::double / nullif(arg_min(avg_stipendio, anno), 0),
                 1.0 / nullif(max(anno) - min(anno), 0)) - 1),
        1
    ) as cagr_pct
from per_anno
group by 1, 2;
