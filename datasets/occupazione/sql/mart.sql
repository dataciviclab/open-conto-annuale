select anno, codi_comparto, desc_comparto,
    sum(tp_u + tp_d + pti_u + pti_d + pts_u + pts_d) as tot_dipendenti,
    sum(tp_u + pti_u + pts_u) as tot_uomini,
    sum(tp_d + pti_d + pts_d) as tot_donne,
    count(distinct istituzione) as enti
from clean_input where codi_comparto is not null
group by 1,2,3;
