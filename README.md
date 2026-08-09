# open-conto-annuale — Il personale della PA italiana, aperto e interrogabile

**1,8 milioni di microdati su chi lavora nel pubblico: ente per ente, anno per anno.**

Il Conto Annuale della Ragioneria Generale dello Stato (MEF) raccoglie i dati
di tutto il personale delle pubbliche amministrazioni italiane. Li abbiamo
puliti, normalizzati e resi pubblici.

## Cosa contiene

| | |
|---|---|
| **Enti coperti** | ~13.000 (comuni, ASL, università, regioni, ministeri) |
| **Periodo** | 2020 — 2024 |
| **Righe** | ~1,85 milioni (solo 2024), multi-anno |
| **Costo del lavoro 2024** | €186 miliardi |

### Trend 2020-2024

| Anno | Dipendenti | % Donne |
|---|---|---|
| 2020 | 3.243.499 | 58,8% |
| 2021 | 3.240.397 | 59,1% |
| 2022 | 3.271.447 | 59,4% |
| 2023 | 3.327.854 | 59,8% |
| 2024 | **3.388.794** | **60,2%** |

### Dataset disponibili (14)

assenze · composizione-retribuzione · costo-lavoro · personale (età) ·
anzianità · contrattazione · titoli-studio · distribuzione geografica ·
retribuzione-media · comandati · passaggi · flessibili ·
modalità-flessibile · occupazione

## Esempi di domande

- **Quanti dipendenti pubblici ci sono nel tuo comune?** E quanto costano?
- **Qual è lo stipendio medio per categoria?** Differenze tra nord e sud?
- **Quante assenze per malattia ci sono state nel 2024?** E per genere?
- **Quanti dirigenti under 40 ci sono nella PA?**
- **Quanto è aumentato il costo del lavoro anno dopo anno?**

## Tre modi per accedere ai dati

### 1. Via MCP (toolkit)

I dataset sono accessibili via SQL dal server MCP toolkit del Lab (una query
per ogni slug: `personale`, `assenze`, `occupazione`, ...).

### 2. Via DuckDB diretto

```python
import duckdb
duckdb.sql("""
    SELECT anno, SUM(dipendenti) AS totale
    FROM read_parquet('gs://dataciviclab-clean/conto-annuale/*.parquet')
    GROUP BY anno ORDER BY anno
""").show()
```

### 3. Via download parquet

Bucket pubblico: `gs://dataciviclab-clean/conto-annuale/`

## Partecipa

- **Hai una domanda su questi dati?** Apri una [Discussion](https://github.com/orgs/dataciviclab/discussions/new?category=Domanda)
- **Vuoi contribuire?** Vedi [come contribuire al Lab](https://github.com/dataciviclab/dataciviclab/blob/main/docs/come-contribuire.md)

## Documenti tecnici

- [Pipeline](docs/pipeline.md) — esecuzione, struttura, output
- [Metodologia](docs/metodologia.md) — origini dati, classificazioni
- [Dataset registry](docs/dataset-registry.md) — elenco dataset, mart, accesso
- [Tracciati](docs/Tracciati.pdf) — specifiche ufficiali CSV (fonte RGS)

Questo progetto fa parte di [DataCivicLab](https://github.com/dataciviclab).
