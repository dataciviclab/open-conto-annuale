select
    anno,
    trim(codi_tipo_voce_spesa::varchar) as codi_tipo_voce_spesa,
    trim(codi_voce_spesa::varchar) as codi_voce_spesa,
    trim(desc_voce_spesa) as desc_voce_spesa,
    trim(flag_segno) as flag_segno,
    -- Chiave composita per JOIN con tabelle dati (formato: A035)
    trim(codi_tipo_voce_spesa::varchar) || lpad(trim(codi_voce_spesa::varchar), 3, '0') as voce_spesa
from raw_input;
