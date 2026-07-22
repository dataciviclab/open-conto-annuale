#!/usr/bin/env python3
"""Gate di qualità per open-conto-annuale."""
from __future__ import annotations
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out", "data")

DATASET_MARTS = {
    "assenze": ["assenze_comparti"],
    "composizione-retribuzione": ["retribuzioni_comparti", "retribuzioni_entrate"],
    "costo-lavoro": ["costo_lavoro_comparti"],
    "personale": ["personale_eta_comparti"],
    "anzianita": ["anzianita_comparti"],
    "titoli-studio": ["titoli_studio_comparti"],
    "comandati": ["comandati_comparti"],
    "contrattazione": ["contrattazione_comparti"],
    "flessibili": ["flessibili_comparti"],
    "passaggi": ["passaggi_comparti"],
    "distribuzione": ["distribuzione_comparti"],
    "retribuzione-media": ["retribuzione_media_comparti"],
    "modalita-flessibile": ["modalita_flessibile_comparti"],
}

def check_clean(dataset: str, year: int) -> list[str]:
    errors = []
    path = os.path.join(OUT, "clean", dataset, str(year), f"{dataset.replace('-','_')}_{year}_clean.parquet")
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
        path = os.path.join(OUT, "mart", dataset.replace('-','_'), str(year), f"{t}.parquet")
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", help="Dataset slug")
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--ci", action="store_true")
    args = parser.parse_args()

    if args.all:
        datasets = list(DATASET_MARTS.keys())
    elif args.dataset:
        datasets = [args.dataset]
    else:
        print("Specifica --dataset o --all"); sys.exit(1)

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
