with raw_data as (
    select
        normalize_string(istituzione) as cod_ente,
        normalize_string(contratto) as cod_contratto,
        normalize_string(categoria) as cod_categoria,
        normalize_italian_number(stipendio) as stipendio,
        normalize_italian_number(ria) as ria,
        normalize_italian_number(tredicesima) as tredicesima,
        normalize_italian_number(straordinario) as straordinario,
        normalize_italian_number(indennita_fisse) as indennita_fisse,
        normalize_italian_number(altre_accessorie) as altre_accessorie
    from raw_input
)
select 2024 as anno, rd.cod_ente as istituzione, rd.cod_contratto as contratto,
    rd.cod_categoria as categoria, rd.stipendio, rd.ria, rd.tredicesima,
    rd.straordinario, rd.indennita_fisse, rd.altre_accessorie,
    e.codi_tipo_istituzione, e.codi_istituzione, e.desc_istituzione,
    c.codi_comparto, c.desc_comparto
from raw_data rd
left join read_parquet('{support.enti.mart}') e on rd.cod_ente = e.istituzione
left join read_parquet('{support.comparti.mart}') c on rd.cod_contratto = c.codi_contratto;
