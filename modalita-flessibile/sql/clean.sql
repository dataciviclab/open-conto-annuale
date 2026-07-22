with raw_data as (
    select
        normalize_string(istituzione) as cod_ente,
        normalize_string(contratto) as cod_contratto,
        normalize_string(macrocategoria) as cod_macrocategoria,
        normalize_string(categoria) as cod_categoria,
        normalize_italian_number(tele_lavoro_uomini) as tl_u,
        normalize_italian_number(tele_lavoro_donne) as tl_d,
        normalize_italian_number(pers_lavoro_agile_u) as agile_u,
        normalize_italian_number(pers_lavoro_agile_d) as agile_d,
        normalize_italian_number(pers_coworking_u) as cowork_u,
        normalize_italian_number(pers_coworking_d) as cowork_d,
        normalize_italian_number(soggetti_turnazione_uomini) as turn_u,
        normalize_italian_number(soggetti_turnazione_donne) as turn_d
    from raw_input
)
select 2024 as anno, rd.cod_ente as istituzione, rd.cod_contratto as contratto,
    rd.cod_macrocategoria as macrocategoria, rd.cod_categoria as categoria,
    rd.tl_u, rd.tl_d, rd.agile_u, rd.agile_d, rd.cowork_u, rd.cowork_d, rd.turn_u, rd.turn_d,
    e.codi_tipo_istituzione, e.codi_istituzione, e.desc_istituzione,
    c.codi_comparto, c.desc_comparto
from raw_data rd
left join read_parquet('{support.enti.mart}') e on rd.cod_ente = e.istituzione
left join read_parquet('{support.comparti.mart}') c on rd.cod_contratto = c.codi_contratto;
