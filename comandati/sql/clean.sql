with raw_data as (
    select
        normalize_string(istituzione) as cod_ente,
        normalize_string(contratto) as cod_contratto,
        normalize_string(categoria) as cod_categoria,
        normalize_string(qualifica) as cod_qualifica,
        -- Nomi colonna esatti dal CSV (DOMME è errore battitura fonte)
        normalize_italian_number(comandati_distaccati_uomini) as comand_dist_u,
        normalize_italian_number(comandati_distaccati_domme) as comand_dist_d,
        normalize_italian_number(fuori_ruolo_uomini) as fuori_ruolo_u,
        normalize_italian_number(fuori_ruolo_donne) as fuori_ruolo_d
    from raw_input
)
select {year} as anno,
    rd.cod_ente as istituzione, rd.cod_contratto as contratto,
    rd.cod_categoria as categoria, rd.cod_qualifica as qualifica,
    rd.comand_dist_u, rd.comand_dist_d, rd.fuori_ruolo_u, rd.fuori_ruolo_d,
    e.codi_tipo_istituzione, e.codi_istituzione, e.desc_istituzione,
    c.codi_comparto, c.desc_comparto
from raw_data rd
left join read_parquet('{support.enti.mart}') e on rd.cod_ente = e.istituzione
left join read_parquet('{support.comparti.mart}') c on rd.cod_contratto = c.codi_contratto;
