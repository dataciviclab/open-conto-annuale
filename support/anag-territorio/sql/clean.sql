select
    anno as anno,
    trim(codi_catastale) as codi_catastale,
    trim(desc_codice_catastale) as desc_codice_catastale,
    trim(codi_provincia) as codi_provincia,
    trim(desc_provincia) as desc_provincia,
    trim(codi_regione) as codi_regione,
    trim(desc_regione) as desc_regione,
    -- Codice regione ISTAT: R00090 → 03 (Lombardia)
    -- Mapping fisso (21 regioni, stabile)
    case trim(codi_regione)
        when 'R00018' then '13' when 'R00027' then '17'
        when 'R00036' then '18' when 'R00045' then '15'
        when 'R00054' then '08' when 'R00063' then '06'
        when 'R00072' then '12' when 'R00081' then '07'
        when 'R00090' then '03' when 'R00107' then '11'
        when 'R00116' then '14' when 'R00125' then '01'
        when 'R00134' then '16' when 'R00143' then '20'
        when 'R00152' then '19' when 'R00161' then '09'
        when 'R00189' then '10' when 'R00198' then '02'
        when 'R00205' then '05' when 'R00214' then '04'
        when 'R00223' then '04'  -- PA Trento e PA Bolzano → Trentino (04)
        else null
    end as codice_regione_istat
from raw_input;
