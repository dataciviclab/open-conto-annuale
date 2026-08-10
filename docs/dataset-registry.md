# Dataset Registry — open-conto-annuale

Registry generato: `registry/registry.json` (fusion ADR, toolkit v1.49+).

Rigenerazione: `toolkit registry build --prefix conto-annuale --write` (o `make registry`).

## Dataset

| Slug | Descrizione | Periodo | Mart |
|---|---|---|---|
| `personale` | Distribuzione per fascia di età del personale PA | 2020–2024 | `personale_eta_comparti` |
| `anzianita` | Anzianità di servizio del personale PA | 2020–2024 | `anzianita_comparti` |
| `assenze` | Giornate di assenza per causale | 2020–2024 | `assenze_comparti` |
| `costo_lavoro` | Costo del lavoro per voce di spesa | 2020–2024 | `costo_lavoro_comparti` |
| `composizione_retribuzione` | Importi retributivi per voce di spesa | 2020–2024 | `retribuzioni_comparti`, `retribuzioni_entrate` |
| `contrattazione` | Spese di contrattazione integrativa | 2020–2024 | `contrattazione_comparti` |
| `titoli_studio` | Titoli di studio del personale PA | 2020–2024 | `titoli_studio_comparti` |
| `comandati` | Personale comandato/fuori ruolo | 2020–2024 | `comandati_comparti` |
| `flessibili` | Lavoratori flessibili per tipologia | 2020–2024 | `flessibili_comparti` |
| `passaggi` | Passaggi di qualifica | 2020–2024 | `passaggi_comparti` |
| `distribuzione` | Distribuzione geografica per regione | 2020–2024 | `distribuzione_comparti` |
| `retribuzione_media` | Retribuzione media per componente | 2020–2024 | `retribuzione_media_comparti` |
| `modalita_flessibile` | Telelavoro, lavoro agile, coworking | 2021–2024 | `modalita_flessibile_comparti` |
| `occupazione` | Occupazione per regime orario | 2020–2024 | `occupazione_comparti` |

### Anagrafiche di supporto (`support/`)

Dizionari usati dai dataset per arricchimento (join in clean.sql via `{support.*.mart}`):
`ca_anag_enti_seed`, `ca_anag_comparti_seed`, `ca_anag_qualifiche_seed`,
`ca_anag_voci_spesa_seed`, `ca_anag_causali_seed`, `ca_anag_territorio_seed`,
`ca_anag_titoli_studio_seed`, `ca_anag_voci_fua_seed`, `ca_anag_fondi_seed`.

## Accesso

- Parquet locali: `out/data/clean|mart/<slug>/<year>/`
- GCS (pubblicati): `gs://dataciviclab-clean/conto-annuale/` e `gs://dataciviclab-mart/conto-annuale/`
- MCP toolkit: ogni slug è queryable via SQL
