select
    anno,
    codi_comparto,
    desc_comparto,
    codi_macrocategoria,
    desc_macrocategoria,
    codi_tipo_istituzione,
    causale_assenza,
    tipo_causale,
    descrizione_causale,
    count(distinct istituzione) as enti_con_assenze,
    sum(assenze_uomini) as tot_assenze_uomini,
    sum(assenze_donne) as tot_assenze_donne,
    sum(coalesce(assenze_uomini, 0) + coalesce(assenze_donne, 0)) as tot_assenze
from clean_input
where codi_comparto is not null
group by 1, 2, 3, 4, 5, 6, 7, 8, 9;
