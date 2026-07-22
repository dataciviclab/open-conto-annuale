select
    anno,
    codi_comparto,
    desc_comparto,
    codi_tipo_istituzione,
    voce_spesa,
    desc_voce_spesa,
    codi_tipo_voce_spesa,
    count(distinct istituzione) as enti,
    sum(totale_spesa) as tot_spesa
from clean_input
where codi_comparto is not null
group by 1, 2, 3, 4, 5, 6, 7;
