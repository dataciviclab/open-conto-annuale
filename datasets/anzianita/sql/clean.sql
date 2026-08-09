with raw_data as (
    select
        normalize_string(istituzione) as cod_ente,
        normalize_string(contratto) as cod_contratto,
        normalize_string(categoria) as cod_categoria,
        normalize_string(qualifica) as cod_qualifica,
        normalize_string(fascia_anzianita) as fascia,
        normalize_italian_number(uomini) as uomini,
        normalize_italian_number(donne) as donne
    from raw_input
)
select
    {year} as anno,
    rd.cod_ente as istituzione,
    rd.cod_contratto as contratto,
    rd.cod_categoria as categoria,
    rd.cod_qualifica as qualifica,
    rd.fascia,
    rd.uomini, rd.donne,
    e.codi_tipo_istituzione, e.desc_tipo_istituzione, e.codi_istituzione,
    e.desc_istituzione, e.codi_fiscale,
    c.codi_comparto, c.desc_comparto, c.codi_aggregato, c.desc_aggregato, c.desc_contratto,
    q.codi_macrocategoria, q.desc_macrocategoria, q.desc_categoria, q.desc_qualifica
from raw_data rd
left join read_parquet('{support.enti.mart}') e on rd.cod_ente = e.istituzione
left join read_parquet('{support.comparti.mart}') c on rd.cod_contratto = c.codi_contratto
left join read_parquet('{support.qualifiche.mart}') q
    on rd.cod_contratto = q.codi_contratto and rd.cod_categoria = q.codi_categoria and rd.cod_qualifica = q.codi_qualifica;
