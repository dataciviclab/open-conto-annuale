# open-conto-annuale — Il personale della PA italiana, aperto e interrogabile

> **Quante persone lavorano nella PA? Quanto costano? Quali retribuzioni? Assenze, età, titoli di studio.**

open-conto-annuale nasce dai dati del **Conto Annuale** della Ragioneria Generale dello Stato (MEF).
Abbiamo pulito, normalizzato e reso pubblici i microdati sul personale di tutte le pubbliche
amministrazioni italiane.

## 📦 I dati in breve

| Cosa | Quanto |
|---|---|
| **Enti coperti** | ~13.000 (comuni, ASL, università, regioni, ministeri, enti pubblici) |
| **Periodo** | dal 2001 (disponibile: 2024) |
| **Righe processate** | ~1,75 milioni (11 dataset) |
| **Join con anagrafiche** | 100% |
| **Anno** | 2024 |

### Dataset disponibili

| Dataset | Cosa contiene | Righe |
|---|---|---|
| assenze | Giorni di assenza per causale, genere | 196.647 |
| composizione-retribuzione | Scomposizione stipendi per voce spesa | 550.897 |
| costo-lavoro | Totale costo del lavoro per voce | 259.961 |
| personale | Fasce età per categoria e genere | 174.758 |
| anzianita | Anzianità di servizio per fascia | 155.657 |
| titoli-studio | Titoli di studio del personale | 91.943 |
| contrattazione | Spese contrattazione integrativa | 215.242 |
| distribuzione | Distribuzione geografica per regione | 62.765 |
| comandati | Personale in comando/fuori ruolo/esonero | 16.263 |
| flessibili | Lavoro tempo determinato, interinale, LSU | 11.306 |
| passaggi | Passaggi di qualifica | 17.131 |

## 🚀 Come eseguire

```bash
# Prerequisiti: Python 3.12+, toolkit installato
pip install git+https://github.com/dataciviclab/toolkit.git

# 1. Scarica lo ZIP annuale (14 MB)
make download

# 2. Estrai i CSV
make extract-dati

# 3. Processa anagrafiche + dati
make seeds
make run-all
```

## 📚 Documenti

- [Pipeline](docs/pipeline.md) — esecuzione, struttura, output
- [Metodologia](docs/metodologia.md) — origini dati, classificazioni, trasformazioni
- [Tracciati](docs/Tracciati.pdf) — specifiche ufficiali dei file CSV (fonte RGS)

## 🏛️ DataCivicLab

open-conto-annuale è un progetto di [DataCivicLab](https://github.com/dataciviclab) —
un laboratorio civico di dati aperti italiani.
