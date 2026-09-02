-- Mart: piramide età per anno
-- Aggrega il clean layer per fascia di età, genere e anno.
-- Il clean ha uomini/donne per ogni fascia → piramide età.

with base as (
    select
        anno,
        fascia,
        sum(uomini) as tot_uomini,
        sum(donne) as tot_donne,
        sum(uomini) + sum(donne) as tot_fascia,
        count(distinct istituzione) as enti
    from clean_input
    group by anno, fascia
)
select
    anno,
    fascia,
    tot_uomini,
    tot_donne,
    tot_fascia,
    round(tot_donne * 100.0 / tot_fascia, 1) as pct_donne,
    enti
from base
order by anno, fascia
