#!/usr/bin/env python3
"""Scarica lo ZIP del Conto Annuale per un dato anno.

Riutilizza lab_connectors.http.download() per il download
con retry, proxy e fallback SSL già gestiti.

Usage:
  python3 scripts/download_zip.py               # anno 2024
  python3 scripts/download_zip.py 2023          # anno specifico
"""
import sys, pathlib

REPO = pathlib.Path(__file__).parent.parent


def main():
    year = sys.argv[1] if len(sys.argv) > 1 else "2024"
    zippath = REPO / f"{year}Tutto.zip"
    if zippath.exists():
        print(f"✅ {zippath.name} già presente ({zippath.stat().st_size // 1024 // 1024} MB)")
        return

    print(f"⬇️  Download {year}Tutto.zip...")
    try:
        from lab_connectors.http import download
        data = download(
            f"https://contoannuale.rgs.mef.gov.it/ext/download/{year}Tutto.zip",
            timeout=180, max_retries=3,
        )
    except ImportError:
        import urllib.request
        print("  (lab_connectors non trovato, uso urllib)")
        resp = urllib.request.urlopen(
            f"https://contoannuale.rgs.mef.gov.it/ext/download/{year}Tutto.zip",
            timeout=180
        )
        data = resp.read()

    zippath.write_bytes(data)
    mb = len(data) / 1024 / 1024
    print(f"✅ Scaricato: {zippath.name} ({mb:.0f} MB)")


if __name__ == "__main__":
    main()
