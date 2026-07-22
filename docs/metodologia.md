# Metodologia — Conto Annuale RGS

## Origine dei dati

I dati provengono dal **Conto Annuale** della Ragioneria Generale dello Stato (MEF),
pubblicati sul portale SICO all'indirizzo:
[https://contoannuale.rgs.mef.gov.it/web/sicosito/download](https://contoannuale.rgs.mef.gov.it/web/sicosito/download)

Il Conto Annuale è la rilevazione censuaria del personale delle pubbliche amministrazioni
italiane. Ogni ente trasmette annualmente i dati relativi a:

- Composizione del personale (occupazione, assunzioni, cessazioni)
- Costo del lavoro e retribuzioni
- Assenze e formazione
- Anzianità, età, titoli di studio
- Contrattazione integrativa
- Lavoro flessibile e modalità di lavoro
- Passaggi di qualifica
- Distribuzione geografica

Copertura: **dal 2001** sull'intero perimetro delle PA italiane.

Il portale genera file ZIP su richiesta (`Tutto.zip`, `Anagrafiche.zip`, `Dati.zip`)
con tutti i microdati in formato CSV per l'anno selezionato.

## Struttura del dataset

Il repository contiene:

- `{year}Tutto.zip` — file ZIP annuale con tutti i CSV (dati + anagrafiche)
- `anagrafica/_data/` — anagrafiche in formato CSV (in git, ~1.6 MB)
- `_local/seed/dati/` — dati estratti dallo ZIP (gitignorati, rigenerabili via `make extract-dati`)
- `out/data/` — output della pipeline (gitignorato)

## Granularità

Ogni tabella BDAP ha una riga per combinazione dimensionale unica (>99.8%).
Le dimensioni comuni sono:

- **ISTITUZIONE**: codice ente (formato: tipo + codice numerico, es. `C3363`)
- **CONTRATTO**: codice contratto collettivo (es. `RALN`, `MNST`, `SSNA`, `UNIV`)
- **CATEGORIA**: categoria di inquadramento (es. `IR`, `EQ`, `OE`, `DI`)
- **QUALIFICA**: qualifica professionale specifica (es. `0IR000`, `0FZEQF`)

### Granularità specifiche per tabella

| Tabella | Dimensione extra |
|---|---|
| ASSENZE | causale_assenza |
| COMPOSIZIONE_RETRIBUZIONE | voce_spesa |
| COSTO_LAVORO | voce_spesa (senza categoria/qualifica) |
| ETA/ANZIANITA | fascia (età/anzianità) |
| TITOLI_STUDIO_DATI | titolo_studio |
| CONTRATTAZIONE_INTEGRATIVA | macrocategoria, tipo_voce, natura, fondo, voce_fua |
| LAVORO_FLESSIBILE | macrocategoria (senza qualifica) |
| PASSAGGI_QUALIFICA | categoria/qualifica partenza → arrivo |
| DISTRIBUZIONE_GEOGRAFICA | regione |

## Trasformazioni chiave

### ISTITUZIONE → ente
Nelle tabelle dati il codice ente è in formato `TIPO+CODICE` (es. `C3363`).
Nell'anagrafica enti i due componenti sono separati:
`CODI_TIPO_ISTITUZIONE` (C, U, IP, OL, ...) e `CODI_ISTITUZIONE` (numerico).
Il seed `anag-enti` genera la colonna `istituzione` come chiave composita
per la JOIN diretta.

### Voce di spesa
Nella tabella VoceSpesa, i codici hanno due componenti: tipo (A, F, T, ...)
e codice (015, 101, ...). Le tabelle dati usano il formato composito `A015`.
Il seed `anag-voci-spesa` genera la colonna `voce_spesa` come
`codi_tipo_voce_spesa || LPAD(codi_voce_spesa, 3, '0')`.

### Codice regione
BDAP usa formato `Rxxxxx` (es. `R00090` = Lombardia, `R00143` = Sardegna).
Il mapping verso il codice ISTAT numerico a 2 cifre è gestito nel
seed `anag-territorio` tramite `CASE` esplicito sulle 21 regioni/province.

### Normalizzazione numeri
I numeri italiani (virgola decimale, punti migliaia) sono gestiti tramite
la macro DuckDB `normalize_italian_number()` del toolkit — carica
automaticamente in ogni clean.sql.

## Join extra-dataset (verso registry del Lab)

| Chiave BDAP | Registry Lab | Tipo |
|---|---|---|
| `CODI_ISTITUZIONE` (es. `C3363`) | `bdap_anagrafe_enti` | Codice ente BDAP diretto |
| `CODI_FISCALE` | `ipa_enti` | CF/Partita IVA ente |
| `CODI_CATASTALE` | `istat_elenco_comuni` / `comuni_master` | Codice catastale → ISTAT |
| `CODI_PROVINCIA` (sigla) | `istat_elenco_comuni` | Sigla provincia 2 char |
| `CODI_REGIONE` (`Rxxxxx`) | `istat_elenco_comuni` | Mapping via anag-territorio |

## Pipeline

La pipeline usa il toolkit DataCivicLab con:

- **Source**: `local_file` → punta ai CSV in `anagrafica/_data/` (seed) o `_local/seed/dati/{year}/` (dati)
- **Clean SQL**: normalizza con macro standard (`normalize_string`, `normalize_italian_number`)
  e join con support dataset via `read_parquet('{support.enti.mart}')`
- **Anno dinamico**: `{year} as anno` nei clean.sql — il toolkit sostituisce `{year}` con l'anno in elaborazione
- **Support fissi**: le anagrafiche hanno `years: [2024]` e vengono usate per tutti gli anni del dataset.
  Le descrizioni (comparti, qualifiche, voci) sono quelle del 2024, scelta intenzionale per
  garantire stabilità classificatoria nelle analisi longitudinali.
- **Mart SQL**: aggregazione per comparto con `clean_input`
