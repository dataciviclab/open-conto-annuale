# Copertura temporale — tier schema Conto Annuale

**Aggiornato**: 2026-10-09  
**Stato**: survey su campioni 2001–2014 (zip reali dal portale RGS); pipeline attuale **2011–2024**

## Disponibilità portale

URL: `https://contoannuale.rgs.mef.gov.it/ext/CSV/{year}Tutto.zip`  
Anni con zip validi (magic `PK`): **2001–2024**. Il 2025 non è ancora pubblicato.

## Tier di schema (per estrazione/normalizzazione)

| Tier | Anni campionati | Formato ZIP | Header | Trattamento extract |
|---|---|---|---|---|
| **Modern** | 2001–2005, 2010–2013, 2017–2024 | flat (≤2005) / nested (2010+) | UPPER_SNAKE, `Fascia Età` | Nessun rename; nested gestito |
| **Pre-2017** | 2004?–2016 (campionato 2014–2016) | flat | Title Case + spazi; ETA bug `Fascia Anzianità`; `TITOLO_STUDIO` | `_style_header` + `_HEADER_OVERRIDES_PRE2017` |

**Boundary inatteso**: il 2013 è già moderno; il **2014 torna pre-2017** (flat, Title Case); 2015–2016 pre-2017; 2017+ moderno. Non assumere monotonia temporale.

## Tabelle mancanti / varianti pre-2010

Campionato 2001 e 2005 (modern-like):

- **Mancante**: `CONTRATTAZIONE_INTEGRATIVA` (dataset `contrattazione` non estendibile senza survey dedicata)
- **Naming**: `TITOLI_STUDIO` (no `_DATI`) — il rename in extract copre già il caso pre-2017; per il tier moderno early serve verificare
- **Typo fonte**: `PERSONALE_TEMPO_PIEDO_DONNE` presente anche nel 2001/2005 (non solo 2017–2020) — `apply_fixes` ora è sempre-on (no-op se assente)
- **Extra non mappati**: `ANZIANITA_MEDIA`, `ASSENZE_MEDIE`, `ETA_MEDIA`, `FORMAZIONE`, `FASCE_RETRIBUZIONE`

## Righe vuote fonte

Alcuni CSV (es. `LAVORO_FLESSIBILE_2013`) contengono righe solo-delimitatore (`;;;;;;;;`).  
`_drop_empty_rows` in `extract_dati.py` le scarta; altrimenti le validazioni clean falliscono su `istituzione`/`contratto` NULL.

## Join anagrafiche (limite noto)

Le anagrafiche di supporto sono fissate al **2024** (`support/*/years: [2024]`), scelta di stabilità classificatoria.

| Colonna join | 2011–2017 (circa) | 2024 |
|---|---|---|
| comparto | ~100% | 100% |
| qualifiche | ~15–17% | 100% |
| voci spesa | ~92–97% | 100% |

Non è una regressione di pipeline: i codici anagrafici storici non matchano il dizionario 2024. Per analisi che richiedono descrittivi qualifica/voce sugli anni storici serve un follow-up con anagrafiche year-specific (dai singoli zip annuali).

## Ondata consigliata per 2001–2010

1. **Survey header** per anno o tier (non fidarsi della monotonia)
2. Escludere o specializzare `contrattazione` dove la tabella manca
3. Estendere `years` per-dataset in base alle tabelle presenti, non una lista unica
4. Poi run pilota 1–2 dataset per anno campione prima del full

## Riferimenti

- Survey matrice header 2015/16/17: `_local/generated/oca_schema_matrix.json` (locale, gitignorato)
- Estrazione: `scripts/extract_dati.py`
- PR 2015–2016: #17 · Branch ondata 2011–2014: `feat/copertura-2011-2014`
