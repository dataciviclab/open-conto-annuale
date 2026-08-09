select
    anno,
    codi_comparto,
    desc_comparto,
    codi_macrocategoria,
    desc_macrocategoria,
    codi_tipo_istituzione,
    voce_spesa,
    desc_voce_spesa,
    codi_tipo_voce_spesa,
    count(distinct istituzione) as enti,
    sum(importo) as tot_importo
from clean_input
where codi_comparto is not null
group by 1, 2, 3, 4, 5, 6, 7, 8, 9;
