-- mart_sintesi — Occupazione per comparto e anno
--
-- Grano: comparto × anno. Risponde: quanti dipendenti per comparto, quota
-- donne e incidenza part-time. 1 riga = 1 (anno, comparto).

select
    anno,
    codi_comparto,
    desc_comparto,
    sum(tp_u + tp_d + pti_u + pti_d + pts_u + pts_d) as tot_dipendenti,
    sum(tp_u + pti_u + pts_u) as tot_uomini,
    sum(tp_d + pti_d + pts_d) as tot_donne,
    round(100.0 * sum(tp_d + pti_d + pts_d) / nullif(sum(tp_u + tp_d + pti_u + pti_d + pts_u + pts_d), 0), 1) as pct_donne,
    sum(pti_u + pti_d + pts_u + pts_d) as tot_part_time,
    round(100.0 * sum(pti_u + pti_d + pts_u + pts_d)
          / nullif(sum(tp_u + tp_d + pti_u + pti_d + pts_u + pts_d), 0), 1) as pct_part_time,
    count(distinct istituzione) as enti
from clean_input
where codi_comparto is not null
group by 1, 2, 3;
