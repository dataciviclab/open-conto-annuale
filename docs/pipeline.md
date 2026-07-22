# Pipeline open-conto-annuale

## Architettura

La pipeline segue il pattern del toolkit DataCivicLab:

```
RAW ──(SQL: clean.sql)──> CLEAN ──(SQL: mart_*.sql)──> MART
```

Ogni dataset (occupazione, assenze, retribuzioni, ...) ha un proprio `dataset.yml`
che descrive l'intera trasformazione. Le anagrafiche sono `support dataset` condivisi,
eseguiti prima dei dataset dati.

## Esecuzione

```bash
# 1. Seeds anagrafici (9 support dataset)
make seeds

# 2. Dataset dati (uno per volta o tutti)
make run-assenze
make run-retribuzioni
make run-personale
make run-all

# 3. Verifica output
make verify
```

## Dataset disponibili

| Dataset | Tabelle BDAP | Granularità | Righe 2024 |
|---|---|---|---|
| occupazione | OCCUPAZIONE + ASSUNTI + CESSATI | (ente, contratto, cat, qualif) | ~113k |
| assenze | ASSENZE + ASSENZE_MEDIE + FORMAZIONE | (ente, contratto, cat, qualif, causale) | ~455k |
| retribuzioni | COMPOSIZIONE_RETRIBUZIONE + COSTO_LAVORO + RETRIBUZIONE_MEDIA | mista (più mart) | ~877k |
| personale | ETA + ANZIANITA + TITOLI_STUDIO + COMANDATI + FASCE | (ente, contratto, cat, qualif) + fascia | ~770k |
| flessibili | LAVORO_FLESSIBILE + MODALITA | (ente, contratto, mcat, cat) | ~19k |
| contrattazione | CONTRATTAZIONE_INTEGRATIVA | 7 dimensioni | ~215k |
| passaggi | PASSAGGI_QUALIFICA | (ente, contratto, cat_part→arr, qual_part→arr, tipo) | ~17k |
| distribuzione | DISTRIBUZIONE_GEOGRAFICA_COMPARTO | (regione, ente, contratto, cat, qualif) | ~63k |

## Support dataset (anagrafiche)

| Seed | Tabella BDAP | Chiave |
|---|---|---|
| anag-enti | TipoIstituzione_Istituzione | CODI_TIPO_ISTITUZIONE + CODI_ISTITUZIONE |
| anag-comparti | CompartoContratto | CODI_CONTRATTO |
| anag-qualifiche | ContrattoMacroCCategQualif | CODI_MACROCATEGORIA, CODI_CATEGORIA, CODI_QUALIFICA |
| anag-voci-spesa | VoceSpesa | CODI_TIPO_VOCE_SPESA, CODI_VOCE_SPESA |
| anag-causali | Causali | CODICE_CAUSALE |
| anag-territorio | RegioneProvinciaCatasto | CODI_CATASTALE, CODI_PROVINCIA, CODI_REGIONE |
| anag-titoli-studio | Titoli_Studio | CODI_TITOLO |
| anag-voci-fua | Voci_Spesa_FUA | CODI_VOCE_SPESA_FUA |
| anag-fondi | Natura_Fondo | CODI_FONDO, CODI_NATURA |

## Output

```
out/data/
├── clean/{dataset}/{year}/{dataset}_{year}_clean.parquet
├── mart/{dataset}/{year}/{table}.parquet
└── _runs/{dataset}/{year}/{run_id}.json
```

## Fonte dati

I dati provengono da **OpenBDAP** (Ragioneria Generale dello Stato — MEF):
`https://bdap-opendata.rgs.mef.gov.it/`
