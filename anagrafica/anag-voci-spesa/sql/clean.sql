select
    anno,
    trim(codi_tipo_voce_spesa::varchar) as codi_tipo_voce_spesa,
    trim(codi_voce_spesa::varchar) as codi_voce_spesa,
    trim(desc_voce_spesa) as desc_voce_spesa,
    trim(flag_segno) as flag_segno
from raw_input;
