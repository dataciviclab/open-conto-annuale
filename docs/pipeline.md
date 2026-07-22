# Pipeline open-conto-annuale

## Architettura

La pipeline segue il pattern del toolkit DataCivicLab:

```
ZIP ──(extract)──> CSV ──(SQL: clean.sql)──> CLEAN ──(SQL: mart_*.sql)──> MART
```

Ogni dataset (assenze, retribuzioni, personale, ...) ha un proprio `dataset.yml`
che descrive l'intera trasformazione RAW → CLEAN → MART. I CSV vengono estratti
dallo ZIP annuale (`{year}Tutto.zip`) scaricato dal sito del Conto Annuale RGS.

Le anagrafiche sono `support dataset` condivisi tra tutti i dataset dati,
eseguiti prima di questi ultimi.

## Setup iniziale

```bash
# 1. Scarica lo ZIP annuale (una tantum)
make download

# 2. Estrae i CSV dati dallo ZIP
make extract-dati

# 3. Processa le anagrafiche (6 seed)
make seeds
```

## Esecuzione

```bash
# Dataset dati (uno per volta)
make run-assenze
make run-composizione-retribuzione
make run-costo-lavoro
make run-personale

# Oppure tutti
make run-all

# Verifica output
make verify
```

I target `run-*` includono automaticamente `extract-dati` come dipendenza.

## Dataset disponibili

| Dataset | Tabella BDAP | Granularità | Righe 2024 | Join |
|---|---|---|---|---|
| assenze | ASSENZE | (ente, contratto, cat, qualif, causale) | 196.647 | 100% |
| composizione-retribuzione | COMPOSIZIONE_RETRIBUZIONE | (ente, contratto, cat, qualif, voce) | 550.897 | 100% |
| costo-lavoro | COSTO_LAVORO | (ente, contratto, voce) | 259.961 | 100% |
| personale | ETA | (ente, contratto, cat, qualif, fascia età) | 174.758 | 100% |
| anzianita | ANZIANITA | (ente, contratto, cat, qualif, fascia anz.) | 155.657 | 100% |
| titoli-studio | TITOLI_STUDIO_DATI | (ente, contratto, cat, qualif, titolo) | 91.943 | 100% |
| comandati | COMANDATI_FUORI_RUOLO_ESONERI | (ente, contratto, cat, qualif) | 16.263 | 100% |
| contrattazione | CONTRATTAZIONE_INTEGRATIVA | 7 dimensioni | 215.242 | 100% |
| flessibili | LAVORO_FLESSIBILE | (ente, contratto, mcat, cat) | 11.306 | 100% |
| passaggi | PASSAGGI_QUALIFICA | (ente, contratto, cat→cat, tipo) | 17.131 | 100% |
| distribuzione | DISTRIBUZIONE_GEOGRAFICA_COMPARTO | (regione, ente, contratto, cat, qualif) | 62.765 | 100% |
| **TOTALE** | | | **~1.752.570** | |

> Nota: `occupazione` (OCCUPAZIONE + ASSUNTI + CESSATI) è già presente come
> dataset `dipendenti_pubblici` in dataset-incubator (2010-2023).
> Il porting nel nuovo pattern è in programma.

## Support dataset (anagrafiche)

| Seed | Tabella BDAP | Chiave | Righe |
|---|---|---|---|
| anag-enti | TipoIstituzione_Istituzione | CODI_TIPO_ISTITUZIONE + CODI_ISTITUZIONE | 12.843 |
| anag-comparti | CompartoContratto | CODI_CONTRATTO | 48 |
| anag-qualifiche | ContrattoMacroCCategQualif | CODI_MACROCATEGORIA, CODI_CATEGORIA, CODI_QUALIFICA | 1.466 |
| anag-voci-spesa | VoceSpesa | CODI_TIPO_VOCE_SPESA, CODI_VOCE_SPESA (con chiave composita) | 179 |
| anag-causali | Causali | CODICE_CAUSALE | 30 |
| anag-territorio | RegioneProvinciaCatasto | CODI_CATASTALE, CODI_PROVINCIA, CODI_REGIONE (+ mapping ISTAT) | 7.902 |

## Output

```
out/data/
├── clean/{dataset}/{year}/{dataset}_{year}_clean.parquet
├── mart/{dataset}/{year}/{table}.parquet
└── _runs/{dataset}/{year}/{run_id}.json
```

I mart sono aggregati per comparto (codi_comparto + desc_comparto).

## Makefile targets

| Comando | Cosa fa |
|---|---|
| `make download` | Scarica `{year}Tutto.zip` dal sito RGS |
| `make extract-dati` | Estrae i CSV dati dallo ZIP in `_local/seed/dati/` |
| `make seeds` | Processa le 6 anagrafiche |
| `make run-{dataset}` | extract-dati + pipeline dataset |
| `make run-all` | seeds + tutti i dataset |
| `make check` | Valida sintassi di tutti i dataset.yml |
| `make verify` | Verifica output (soglie minime) |
| `make smoke` | Smoke test (sample 1000 righe) |
| `make clean` | Rimuove output |

## Fonte dati

Il file ZIP (`{year}Tutto.zip`) viene scaricato dal portale del Conto Annuale RGS:
`https://contoannuale.rgs.mef.gov.it/web/sicosito/download`

Contiene tutti i microdati (anagrafiche + dati) in formato CSV per l'anno selezionato,
generato su richiesta dal portale Liferay della Ragioneria Generale dello Stato (MEF).

Documentazione ufficiale dei tracciati: `docs/Tracciati.pdf`
