# open-conto-annuale — Il personale della PA italiana, aperto e interrogabile

> **Quante persone lavorano nella PA? Quanto costano? Quali retribuzioni? Assenze, età, titoli di studio.**

open-conto-annuale nasce dai dati del **Conto Annuale** della Ragioneria Generale dello Stato (MEF).
Abbiamo pulito, normalizzato e reso pubblici i microdati sul personale di tutte le pubbliche
amministrazioni italiane.

## 📦 I dati in breve

| Cosa | Quanto |
|---|---|
| **Enti coperti** | ~13.000 (comuni, ASL, università, regioni, ministeri, enti pubblici) |
| **Periodo** | 2020 — 2024 (disponibili dal 2001) |
| **Righe processate** | ~1,8 milioni (2024), multi-anno |
| **Join con anagrafiche** | 100% su tutti i dataset |
| **Anni** | 2020, 2021, 2022, 2023, 2024 |

### Dataset

| Dataset | Cosa contiene | Righe 2024 |
|---|---|---|
| **assenze** | Giorni di assenza per causale, genere | 196.647 |
| **composizione-retribuzione** | Scomposizione stipendi per voce spesa | 550.897 |
| **costo-lavoro** | Totale costo del lavoro per voce | 259.961 |
| **personale** (età) | Fasce età per categoria e genere | 174.758 |
| **anzianita** | Anzianità di servizio per fascia | 155.657 |
| **contrattazione** | Spese contrattazione integrativa | 215.242 |
| **titoli-studio** | Titoli di studio del personale | 91.943 |
| **distribuzione** | Distribuzione geografica per regione | 62.765 |
| **retribuzione-media** | Stipendi medi pro-capite per categoria | 33.619 |
| **comandati** | Personale in comando, fuori ruolo, esonero | 16.263 |
| **passaggi** | Passaggi di qualifica | 17.131 |
| **flessibili** | Lavoro tempo determinato, interinale, LSU | 11.306 |
| **modalita-flessibile** | Telelavoro, lavoro agile, coworking | 8.169 |
| **occupazione** | Dipendenti per ente, contratto, categoria, qualifica | 52.914 |
| **TOTALE** | | **~1,85M** |

## 🚀 Come eseguire

```bash
# Prerequisiti: Python 3.12+, toolkit installato
pip install git+https://github.com/dataciviclab/toolkit.git

# Scarica lo ZIP annuale (13-21 MB l'uno)
make download              # solo 2024
make download YEARS="2020 2021 2022 2023 2024"  # tutti

# Estrai i CSV
make extract-dati          # solo 2024
YEARS="2020 2021 2022 2023 2024" make extract-dati

# Processa anagrafiche + dati
make seeds
make run-all               # tutti i dataset, tutti gli anni
```

### Comandi disponibili

| Comando | Cosa fa |
|---|---|
| `make download` | Scarica ZIP annuale dal sito RGS |
| `make extract-dati` | Estrae CSV in `_local/seed/dati/{year}/` |
| `make seeds` | Processa le 9 anagrafiche |
| `make run-{dataset}` | Processa un dataset (es. `run-assenze`) |
| `make run-all` | Processa tutti i 13 dataset |
| `make check` | Valida sintassi di tutti i config |
| `make verify` | Verifica output (soglie minime righe) |
| `make smoke` | Smoke test (sample 1000 righe) |
| `make clean` | Rimuove output |

## 📊 Trend 2020-2024 in pillole

| Anno | Dipendenti | Δ anno | % Donne | Saldo ass/cas |
|---|---|---|---|---|
| 2020 | 3.243.499 | — | 58,8% | -30.170 |
| 2021 | 3.240.397 | -3.102 | 59,1% | -8.578 |
| 2022 | 3.271.447 | +31.050 | 59,4% | +7.313 |
| 2023 | 3.327.854 | +56.407 | 59,8% | +55.966 |
| 2024 | 3.388.794 | +60.940 | 60,2% | +42.584 |

**Costo del lavoro 2024**: €186 miliardi.

## 📚 Documenti

- [Pipeline](docs/pipeline.md) — esecuzione, struttura, output
- [Metodologia](docs/metodologia.md) — origini dati, classificazioni, trasformazioni
- [Tracciati](docs/Tracciati.pdf) — specifiche ufficiali dei file CSV (fonte RGS)

## 🏛️ DataCivicLab

open-conto-annuale è un progetto di [DataCivicLab](https://github.com/dataciviclab) —
un laboratorio civico di dati aperti italiani.
