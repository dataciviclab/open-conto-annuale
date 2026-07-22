select anno, codi_comparto, desc_comparto,
    sum(td_u) as tot_td_u, sum(td_d) as tot_td_d,
    sum(fl_u) as tot_fl_u, sum(fl_d) as tot_fl_d,
    sum(int_u) as tot_int_u, sum(int_d) as tot_int_d,
    sum(lsu_u) as tot_lsu_u, sum(lsu_d) as tot_lsu_d,
    count(distinct istituzione) as enti
from clean_input where codi_comparto is not null group by 1,2,3;
