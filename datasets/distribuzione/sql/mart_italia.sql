-- Mart: distribuzione per regione × anno
-- Aggrega il clean layer per regione, comparto e anno.
-- Join con anagrafica territorio per avere i nomi delle regioni.

with base as (
    select
        anno,
        regione,
        codi_comparto,
        desc_comparto,
        sum(uomini) as tot_uomini,
        sum(donne) as tot_donne,
        sum(uomini) + sum(donne) as tot_dipendenti,
        count(distinct istituzione) as enti
    from clean_input
    group by anno, regione, codi_comparto, desc_comparto
),
regioni as (
    select distinct codi_regione, desc_regione
    from read_parquet('{support.territorio.mart}')
),
totale_nazionale as (
    select
        anno,
        sum(tot_dipendenti) as tot_nazionale
    from base
    group by anno
)
select
    b.anno,
    coalesce(r.desc_regione, b.regione) as regione,
    b.regione as codi_regione,
    b.codi_comparto,
    b.desc_comparto,
    b.tot_uomini,
    b.tot_donne,
    b.tot_dipendenti,
    round(b.tot_donne * 100.0 / b.tot_dipendenti, 1) as pct_donne,
    round(b.tot_dipendenti * 100.0 / t.tot_nazionale, 1) as pct_nazionale,
    b.enti
from base b
left join regioni r on b.regione = r.codi_regione
left join totale_nazionale t on b.anno = t.anno
order by b.anno, b.regione, b.tot_dipendenti desc
