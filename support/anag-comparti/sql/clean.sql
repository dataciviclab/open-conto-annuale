select
    anno as anno,
    trim(codi_comparto) as codi_comparto,
    trim(desc_comparto) as desc_comparto,
    trim(codi_aggregato) as codi_aggregato,
    trim(desc_aggregato) as desc_aggregato,
    trim(codi_contratto) as codi_contratto,
    trim(desc_contratto) as desc_contratto
from raw_input;
