with raw_data as (
    select
        normalize_string(istituzione) as cod_ente,
        normalize_string(contratto) as cod_contratto,
        normalize_string(voce_spesa) as cod_voce_spesa,
        normalize_italian_number(totale_spesa) as totale_spesa
    from raw_input
)
select
    2024 as anno,
    rd.cod_ente as istituzione,
    rd.cod_contratto as contratto,
    rd.cod_voce_spesa as voce_spesa,
    rd.totale_spesa,
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
    v.codi_tipo_voce_spesa,
    v.desc_voce_spesa,
    v.flag_segno
from raw_data rd
left join read_parquet('{support.enti.mart}') e on rd.cod_ente = e.istituzione
left join read_parquet('{support.comparti.mart}') c on rd.cod_contratto = c.codi_contratto
left join read_parquet('{support.voci_spesa.mart}') v on rd.cod_voce_spesa = v.voce_spesa;
