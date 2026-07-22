select
    vocemart.codi_tipo_voce_spesa,
    vocemart.desc_voce_spesa,
    vocemart.desc_comparto,
    sum(vocemart.importo) as tot_importo,
    count(distinct vocemart.istituzione) as enti
from clean_input vocemart
where vocemart.codi_tipo_voce_spesa is not null
group by 1, 2, 3;
