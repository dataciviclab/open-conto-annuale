select
    anno as anno,
    trim(codi_contratto) as codi_contratto,
    trim(codi_macrocategoria) as codi_macrocategoria,
    trim(desc_macrocategoria) as desc_macrocategoria,
    trim(codi_categoria) as codi_categoria,
    trim(desc_categoria) as desc_categoria,
    trim(codi_qualifica) as codi_qualifica,
    trim(desc_qualifica) as desc_qualifica
from raw_input;
