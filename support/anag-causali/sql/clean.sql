select
    anno as anno,
    trim(codice_tipo_causale) as codice_tipo_causale,
    trim(tipo_causale) as tipo_causale,
    trim(codice_causale) as codice_causale,
    trim(descrizione_causale) as descrizione_causale
from raw_input;
