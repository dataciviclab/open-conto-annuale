#!/usr/bin/env python3
"""Scarica lo ZIP del Conto Annuale per un dato anno.

L'URL di download si ricava dallo JavaScript della pagina:
  https://contoannuale.rgs.mef.gov.it/ext/CSV/{ANNO}{TIPO}
Dove TIPO = Tutto.zip (completo), Anagrafiche.zip, Dati.zip

Usage:
  python3 scripts/download_zip.py               # anno 2024, completo
  python3 scripts/download_zip.py 2023           # anno specifico
  python3 scripts/download_zip.py 2024 Dati.zip  # solo dati
"""
import sys, pathlib, urllib.request

REPO = pathlib.Path(__file__).parent.parent
BASE = "https://contoannuale.rgs.mef.gov.it/ext/CSV/"


def main():
    year = sys.argv[1] if len(sys.argv) > 1 else "2024"
    tipologia = sys.argv[2] if len(sys.argv) > 2 else "Tutto.zip"
    zippath = REPO / f"{year}Tutto.zip"

    if zippath.exists():
        print(f"✅ {zippath.name} già presente ({zippath.stat().st_size // 1024 // 1024} MB)")
        return

    url = f"{BASE}{year}{tipologia}"
    print(f"⬇️  Download {url} ...")

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://contoannuale.rgs.mef.gov.it/web/sicosito/download",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "it-IT,it;q=0.9",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = resp.read()
    except Exception as e:
        print(f"❌ Download fallito: {e}")
        sys.exit(1)

    if len(data) < 10000:
        print(f"❌ Download troppo piccolo ({len(data)} bytes): potrebbe essere un errore")
        sys.exit(1)

    zippath.write_bytes(data)
    mb = len(data) / 1024 / 1024
    print(f"✅ Scaricato: {zippath.name} ({mb:.0f} MB)")


if __name__ == "__main__":
    main()
