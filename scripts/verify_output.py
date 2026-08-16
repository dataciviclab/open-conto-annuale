#!/usr/bin/env python3
"""Gate di qualità per open-conto-annuale. Supporta multi-anno."""
from __future__ import annotations
import argparse, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out", "data")

DATASETS = [
    "assenze", "composizione-retribuzione", "costo-lavoro", "personale",
    "anzianita", "titoli-studio", "comandati", "contrattazione", "flessibili",
    "passaggi", "distribuzione", "retribuzione-media", "modalita-flessibile",
]

# Per ogni dataset: nome del dataset_mart (nel path usa underscore)
def mart_dir(dataset):
    return dataset.replace("-", "_")

def check_clean(dataset: str, year: int):
    errors = []
    clean_name = f"{mart_dir(dataset)}_{year}_clean.parquet"
    path = os.path.join(OUT, "clean", mart_dir(dataset), str(year), clean_name)
    if not os.path.isfile(path):
        errors.append(f"MISSING clean: {path}")
        return errors
    from lab_connectors.duckdb import safe_connect
    with safe_connect() as con:
        try:
            row_count = con.execute(f"SELECT count(*) FROM '{path}'").fetchone()[0]
            if row_count < 100:
                errors.append(f"CLEAN {dataset}/{year}: solo {row_count} righe (min 100)")
            else:
                print(f"  ✅ clean {dataset}/{year}: {row_count:>8,} righe")
        except Exception as e:
            errors.append(f"CLEAN {dataset}/{year}: errore: {e}")
    return errors

def check_mart(dataset: str, year: int):
    errors = []
    dirpath = os.path.join(OUT, "mart", mart_dir(dataset), str(year))
    if not os.path.isdir(dirpath):
        errors.append(f"MISSING mart dir: {dirpath}")
        return errors
    from lab_connectors.duckdb import safe_connect
    with safe_connect() as con:
        for f in os.listdir(dirpath):
            if not f.endswith(".parquet"):
                continue
            path = os.path.join(dirpath, f)
            try:
                row_count = con.execute(f"SELECT count(*) FROM '{path}'").fetchone()[0]
                print(f"  ✅ mart {f}/{year}: {row_count:>8,} righe")
            except Exception as e:
                errors.append(f"MART {f}/{year}: errore: {e}")
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset")
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--ci", action="store_true")
    args = parser.parse_args()

    if args.all:
        datasets = DATASETS
    elif args.dataset:
        datasets = [args.dataset]
    else:
        print("Specifica --dataset o --all"); sys.exit(1)

    all_errors = []
    for ds in datasets:
        print(f"\n📊 {ds} ({args.year}):")
        all_errors += check_clean(ds, args.year)
        all_errors += check_mart(ds, args.year)

    if all_errors:
        print(f"\n❌ {len(all_errors)} errori:")
        for e in all_errors:
            print(f"   • {e}")
        if args.ci:
            sys.exit(1)
    else:
        print(f"\n✅ Tutti i check passati ({len(datasets)} dataset, {args.year})")

if __name__ == "__main__":
    main()
