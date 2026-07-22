with raw_data as (
    select
        normalize_string(regione) as cod_regione,
        normalize_string(istituzione) as cod_ente,
        normalize_string(contratto) as cod_contratto,
        normalize_string(categoria) as cod_categoria,
        normalize_string(qualifica) as cod_qualifica,
        normalize_italian_number(uomini) as uomini,
        normalize_italian_number(donne) as donne
    from raw_input
)
select
    2024 as anno,
    rd.cod_regione as regione,
    rd.cod_ente as istituzione,
    rd.cod_contratto as contratto,
    rd.cod_categoria as categoria,
    rd.cod_qualifica as qualifica,
    rd.uomini, rd.donne,
    e.codi_tipo_istituzione, e.codi_istituzione, e.desc_istituzione,
    c.codi_comparto, c.desc_comparto
from raw_data rd
left join read_parquet('{support.enti.mart}') e on rd.cod_ente = e.istituzione
left join read_parquet('{support.comparti.mart}') c on rd.cod_contratto = c.codi_contratto;
