select anno as anno, normalize_string(codi_contratto) as codi_contratto, normalize_string(codi_tipo_voce_spesa) as codi_tipo_voce_spesa, normalize_string(tipo_voce_spesa) as tipo_voce_spesa, normalize_string(codi_voce_spesa) as codi_voce_spesa, normalize_string(desc_voce_spesa) as desc_voce_spesa, normalize_string(flag_segno) as flag_segno
from raw_input;
