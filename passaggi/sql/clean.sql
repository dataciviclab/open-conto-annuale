with raw_data as (
    select
        normalize_string(istituzione) as cod_ente,
        normalize_string(contratto) as cod_contratto
,       normalize_string(categoria_partenza) as cod_cat_partenza,
        normalize_string(qualifica_partenza) as cod_qual_partenza,
        normalize_string(categoria_arrivo) as cod_cat_arrivo,
        normalize_string(qualifica_arrivo) as cod_qual_arrivo,
        normalize_string(tipo_passaggio) as cod_tipo_passaggio,
        normalize_italian_number(numero_passaggi) as numero_passaggi
    from raw_input
)
select
    2024 as anno,
    rd.cod_ente as istituzione,
    rd.cod_contratto as contratto,
    rd.numero_passaggi,
    rd.cod_cat_partenza as categoria_partenza,
    rd.cod_qual_partenza as qualifica_partenza,
    rd.cod_cat_arrivo as categoria_arrivo,
    rd.cod_qual_arrivo as qualifica_arrivo,
    rd.cod_tipo_passaggio as tipo_passaggio,
    e.codi_tipo_istituzione, e.desc_tipo_istituzione, e.codi_istituzione,
    e.desc_istituzione, e.codi_fiscale,
    c.codi_comparto, c.desc_comparto, c.codi_aggregato, c.desc_aggregato, c.desc_contratto
from raw_data rd
left join read_parquet('{support.enti.mart}') e on rd.cod_ente = e.istituzione
left join read_parquet('{support.comparti.mart}') c on rd.cod_contratto = c.codi_contratto
;