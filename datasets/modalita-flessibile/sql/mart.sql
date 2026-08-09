select anno, codi_comparto, desc_comparto,
    sum(tl_u) as tot_tl_u, sum(tl_d) as tot_tl_d,
    sum(agile_u) as tot_agile_u, sum(agile_d) as tot_agile_d,
    sum(cowork_u) as tot_cowork_u, sum(cowork_d) as tot_cowork_d,
    sum(turn_u) as tot_turn_u, sum(turn_d) as tot_turn_d,
    count(distinct istituzione) as enti
from clean_input where codi_comparto is not null group by 1,2,3;
