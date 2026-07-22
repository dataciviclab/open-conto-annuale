with raw_data as (
    select
        normalize_string(istituzione) as cod_ente,
        normalize_string(contratto) as cod_contratto,
        normalize_string(macrocategoria) as cod_macrocategoria,
        normalize_string(tipo_voce_spesa) as cod_tipo_voce_spesa,
        normalize_string(natura) as cod_natura,
        normalize_string(fondo) as cod_fondo,
        normalize_string(voce_spesa_fua) as cod_voce_spesa_fua,
        normalize_italian_number(importo) as importo
    from raw_input
)
select {year} as anno,
    rd.cod_ente as istituzione, rd.cod_contratto as contratto,
    rd.cod_macrocategoria as macrocategoria,
    rd.cod_tipo_voce_spesa as tipo_voce_spesa, rd.cod_natura as natura,
    rd.cod_fondo as fondo, rd.cod_voce_spesa_fua as voce_spesa_fua,
    rd.importo,
    e.codi_tipo_istituzione, e.codi_istituzione, e.desc_istituzione,
    c.codi_comparto, c.desc_comparto
from raw_data rd
left join read_parquet('{support.enti.mart}') e on rd.cod_ente = e.istituzione
left join read_parquet('{support.comparti.mart}') c on rd.cod_contratto = c.codi_contratto;
