select
    anno,
    trim(codi_tipo_istituzione) as codi_tipo_istituzione,
    trim(desc_tipo_istituzione) as desc_tipo_istituzione,
    try_cast(codi_istituzione as integer) as codi_istituzione,
    trim(desc_istituzione) as desc_istituzione,
    trim(codi_fiscale) as codi_fiscale,
    -- Chiave composita per JOIN con tabelle dati (formato: C3363)
    trim(codi_tipo_istituzione) || trim(codi_istituzione::varchar) as istituzione
from raw_input;
