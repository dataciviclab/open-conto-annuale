select
    anno, codi_comparto, desc_comparto,
    sum(numero_passaggi) as tot_numero_passaggi, count(distinct istituzione) as enti
from clean_input
where codi_comparto is not null
group by 1, 2, 3;
