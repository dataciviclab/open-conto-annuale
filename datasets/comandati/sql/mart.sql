select anno, codi_comparto, desc_comparto,
    sum(comand_dist_u) as tot_comand_dist_u,
    sum(comand_dist_d) as tot_comand_dist_d,
    sum(fuori_ruolo_u) as tot_fuori_ruolo_u,
    sum(fuori_ruolo_d) as tot_fuori_ruolo_d,
    count(distinct istituzione) as enti
from clean_input where codi_comparto is not null group by 1,2,3;
