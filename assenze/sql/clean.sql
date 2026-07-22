with raw_data as (
    select
        normalize_string(istituzione) as cod_ente,
        normalize_string(contratto) as cod_contratto,
        normalize_string(categoria) as cod_categoria,
        normalize_string(qualifica) as cod_qualifica,
        normalize_string(causale_assenza) as cod_causale,
        normalize_italian_number(assenze_uomini) as assenze_uomini,
        normalize_italian_number(assenze_donne) as assenze_donne
    from raw_input
)
select
    2024 as anno,
    rd.cod_ente as istituzione,
    rd.cod_contratto as contratto,
    rd.cod_categoria as categoria,
    rd.cod_qualifica as qualifica,
    rd.cod_causale as causale_assenza,
    rd.assenze_uomini,
    rd.assenze_donne,
    e.codi_tipo_istituzione,
    e.desc_tipo_istituzione,
    e.codi_istituzione,
    e.desc_istituzione,
    e.codi_fiscale,
    c.codi_comparto,
    c.desc_comparto,
    c.codi_aggregato,
    c.desc_aggregato,
    c.desc_contratto,
    q.codi_macrocategoria,
    q.desc_macrocategoria,
    q.desc_categoria,
    q.desc_qualifica,
    ca.codice_tipo_causale,
    ca.tipo_causale,
    ca.descrizione_causale
from raw_data rd
left join read_parquet('{support.enti.mart}') e on rd.cod_ente = e.istituzione
left join read_parquet('{support.comparti.mart}') c on rd.cod_contratto = c.codi_contratto
left join read_parquet('{support.qualifiche.mart}') q
    on rd.cod_contratto = q.codi_contratto
    and rd.cod_categoria = q.codi_categoria
    and rd.cod_qualifica = q.codi_qualifica
left join read_parquet('{support.causali.mart}') ca on rd.cod_causale = ca.codice_causale;
