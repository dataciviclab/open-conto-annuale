# Metodologia — Conto Annuale RGS

## Origine dei dati

I dati provengono dal **Conto Annuale** della Ragioneria Generale dello Stato (MEF),
raccolti tramite il sistema **OpenBDAP** (Banca Dati delle Amministrazioni Pubbliche).

Il Conto Annuale è la rilevazione censuaria del personale delle pubbliche amministrazioni
italiane. Ogni ente trasmette annualmente i dati relativi a:
- Composizione del personale (occupazione, assunzioni, cessazioni)
- Costo del lavoro e retribuzioni
- Assenze e formazione
- Anzianità, età, titoli di studio
- Contrattazione integrativa
- Lavoro flessibile e modalità di lavoro
- Passaggi di qualifica

Copertura: **dal 2001** sull'intero perimetro delle PA italiane.

## Granularità

Ogni tabella BDAP ha una riga per combinazione dimensionale unica. Le dimensioni comuni sono:

- **ISTITUZIONE**: codice ente (formato: tipo + codice numerico, es. `C3363`)
- **CONTRATTO**: codice contratto collettivo (es. `RALN`, `MNST`, `SSNA`, `UNIV`)
- **CATEGORIA**: categoria di inquadramento (es. `IR`, `EQ`, `OE`, `DI`)
- **QUALIFICA**: qualifica professionale specifica (es. `0IR000`, `0FZEQF`)

## Trasformazioni chiave

### ISTITUZIONE → ente
Nelle tabelle dati il codice ente è in formato `TIPO+CODICE` (es. `C3363`).
Nell'anagrafica enti i due componenti sono separati:
`CODI_TIPO_ISTITUZIONE` (C, U, IP, OL, ...) e `CODI_ISTITUZIONE` (numerico).
Il clean.sql riconcilia le due rappresentazioni.

### Codice regione
BDAP usa formato `Rxxxxx` (es. `R00090` = Lombardia). Diverso dal codice ISTAT
numerico a 2 cifre. Il mapping è gestito nel support dataset anag-territorio.

### Gestione encoding
I file BDAP sono in latin-1 con BOM su alcuni header. Il clean.sql normalizza
a UTF-8 e pulisce i nomi colonna.

## Join extra-dataset

| Chiave BDAP | Registry Lab | Notes |
|---|---|---|
| CODI_ISTITUZIONE | `bdap_anagrafe_enti` | Codice ente BDAP diretto |
| CODI_FISCALE | `ipa_enti` | CF/Partita IVA ente |
| CODI_CATASTALE | `istat_elenco_comuni` / `comuni_master` | Codice catastale → ISTAT |
| CODI_PROVINCIA | `istat_elenco_comuni` | Sigla provincia 2 char |
