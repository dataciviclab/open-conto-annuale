#!/usr/bin/env python3
"""
Gate di qualità per open-conto-annuale.

Verifica che ogni dataset dati produca output validi: clean esistente,
join riusciti, soglie minime righe, mart presenti.

Usage:
  python3 scripts/verify_output.py --dataset occupazione --year 2024
  python3 scripts/verify_output.py --all --year 2024
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out", "data")


def check_clean(dataset: str, year: int) -> list[str]:
    errors = []
    path = os.path.join(OUT, "clean", dataset, str(year), f"{dataset}_{year}_clean.parquet")
    if not os.path.isfile(path):
        errors.append(f"MISSING clean: {path}")
        return errors

    import duckdb
    con = duckdb.connect()
    try:
        row_count = con.execute(f"SELECT count(*) FROM '{path}'").fetchone()[0]
        if row_count < 100:
            errors.append(f"CLEAN {dataset}/{year}: solo {row_count} righe (min 100)")
        else:
            print(f"  ✅ clean {dataset}/{year}: {row_count:,} righe")
    except Exception as e:
        errors.append(f"CLEAN {dataset}/{year}: errore lettura: {e}")
    finally:
        con.close()
    return errors


def check_mart(dataset: str, year: int, tables: list[str]) -> list[str]:
    errors = []
    for t in tables:
        path = os.path.join(OUT, "mart", dataset, str(year), f"{t}.parquet")
        if not os.path.isfile(path):
            errors.append(f"MISSING mart: {path}")
            continue
        import duckdb
        con = duckdb.connect()
        try:
            row_count = con.execute(f"SELECT count(*) FROM '{path}'").fetchone()[0]
            print(f"  ✅ mart {t}/{year}: {row_count:,} righe")
        except Exception as e:
            errors.append(f"MART {t}/{year}: errore lettura: {e}")
        finally:
            con.close()
    return errors


def main():
    parser = argparse.ArgumentParser(description="Verifica output pipeline conto annuale")
    parser.add_argument("--dataset", help="Dataset slug (es. assenze)")
    parser.add_argument("--year", type=int, default=2024, help="Anno da verificare")
    parser.add_argument("--all", action="store_true", help="Verifica tutti i dataset")
    parser.add_argument("--ci", action="store_true", help="Modalità CI: exit 1 su errori")
    args = parser.parse_args()

    # Config dataset → mart attesi
    DATASET_MARTS = {
        "assenze": ["assenze_comparti", "assenze_causali"],
        "retribuzioni": ["retribuzioni_comparti"],
        "personale": ["personale_eta", "personale_anzianita"],
        "occupazione": ["occupazione_comparti"],
        "flessibili": ["flessibili_comparti"],
    }

    if args.all:
        datasets = list(DATASET_MARTS.keys())
    elif args.dataset:
        datasets = [args.dataset]
    else:
        print("Specifica --dataset o --all")
        sys.exit(1)

    all_errors = []
    for ds in datasets:
        print(f"\n📊 {ds} ({args.year}):")
        all_errors += check_clean(ds, args.year)
        marts = DATASET_MARTS.get(ds, [])
        if marts:
            all_errors += check_mart(ds, args.year, marts)

    if all_errors:
        print(f"\n❌ {len(all_errors)} errori:")
        for e in all_errors:
            print(f"   • {e}")
        if args.ci:
            sys.exit(1)
    else:
        print(f"\n✅ Tutti i check passati per {', '.join(datasets)} ({args.year})")


if __name__ == "__main__":
    main()
