with raw_data as (
    select
        normalize_string(istituzione) as cod_ente,
        normalize_string(contratto) as cod_contratto,
        normalize_string(macrocategoria) as cod_macrocategoria,
        normalize_string(categoria) as cod_categoria,
        normalize_italian_number(personale_tempo_determinato_uomini) as td_u,
        normalize_italian_number(personale_tempo_determinato_donne) as td_d,
        normalize_italian_number(formazione_lavoro_uomini) as fl_u,
        normalize_italian_number(formazione_lavoro_donne) as fl_d,
        normalize_italian_number(interinale_uomini) as int_u,
        normalize_italian_number(interinale_donne) as int_d,
        normalize_italian_number(lavoro_socialmente_utile_uomini) as lsu_u,
        normalize_italian_number(lavoro_socialmente_utile_donne) as lsu_d
    from raw_input
)
select 2024 as anno,
    rd.cod_ente as istituzione, rd.cod_contratto as contratto,
    rd.cod_macrocategoria as macrocategoria, rd.cod_categoria as categoria,
    rd.td_u, rd.td_d, rd.fl_u, rd.fl_d, rd.int_u, rd.int_d, rd.lsu_u, rd.lsu_d,
    e.codi_tipo_istituzione, e.codi_istituzione, e.desc_istituzione,
    c.codi_comparto, c.desc_comparto
from raw_data rd
left join read_parquet('{support.enti.mart}') e on rd.cod_ente = e.istituzione
left join read_parquet('{support.comparti.mart}') c on rd.cod_contratto = c.codi_contratto;
