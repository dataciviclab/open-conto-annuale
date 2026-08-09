select anno as anno, normalize_string(codi_titolo) as codi_titolo, normalize_string(desc_titolo) as desc_titolo
from raw_input;
