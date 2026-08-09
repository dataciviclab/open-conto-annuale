select anno, codi_comparto, desc_comparto, fascia,
    sum(uomini) as tot_uomini, sum(donne) as tot_donne, count(distinct istituzione) as enti
from clean_input where codi_comparto is not null group by 1,2,3,4;
