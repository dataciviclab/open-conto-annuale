with raw_data as (
    select
        normalize_string(istituzione) as cod_ente,
        normalize_string(contratto) as cod_contratto,
        normalize_string(categoria) as cod_categoria,
        normalize_string(qualifica) as cod_qualifica,
        normalize_italian_number("personale_tempo_pieno_uomini") as tp_u,
        normalize_italian_number("personale_tempo_pieno_donne") as tp_d,
        normalize_italian_number("part_time_inf50%_uomini") as pti_u,
        normalize_italian_number("part_time_inf50%_donne") as pti_d,
        normalize_italian_number("part_time_sup50%_uomini") as pts_u,
        normalize_italian_number("part_time_sup50%_donne") as pts_d
    from raw_input
)
select
    {year} as anno,
    rd.cod_ente as istituzione, rd.cod_contratto as contratto,
    rd.cod_categoria as categoria, rd.cod_qualifica as qualifica,
    rd.tp_u, rd.tp_d, rd.pti_u, rd.pti_d, rd.pts_u, rd.pts_d,
    e.codi_tipo_istituzione, e.codi_istituzione, e.desc_istituzione,
    c.codi_comparto, c.desc_comparto
from raw_data rd
left join read_parquet('{support.enti.mart}') e on rd.cod_ente = e.istituzione
left join read_parquet('{support.comparti.mart}') c on rd.cod_contratto = c.codi_contratto;
