#!/usr/bin/env python3
"""Scarica e estrae i dati del Conto Annuale per un dato anno.

Un unico script che sostituisce download_zip.py + lo step unzip bash:

1. Scarica lo ZIP ``{year}Tutto.zip`` dal sito RGS (1 volta per anno —
   lo ZIP contiene tutti i file di tutti i dataset, scaricarlo N volte
   per N dataset sarebbe uno spreco).
2. Estrae SOLO i file di ``{year}Dati/`` in ``_local/seed/dati/{year}/``.
3. Applica il fix del 2020 (colonna PIEDO → PIENO in OCCUPAZIONE).

Usage:
  python3 scripts/extract_dati.py               # anno 2024
  python3 scripts/extract_dati.py 2020 2021     # più anni
"""
import pathlib
import sys
import urllib.request
import zipfile

REPO = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://contoannuale.rgs.mef.gov.it/ext/CSV/"
OUT_DIR = REPO / "_local" / "seed" / "dati"

# Fix colonna 2020 (errore di battitura della fonte RGS)
FIX_2020 = {
    "OCCUPAZIONE_2020.CSV": [
        ("PERSONALE_TEMPO_PIEDO_DONNE", "PERSONALE_TEMPO_PIENO_DONNE")
    ],
}

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://contoannuale.rgs.mef.gov.it/web/sicosito/download",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "it-IT,it;q=0.9",
}


def download_zip(year: int) -> pathlib.Path:
    """Scarica lo ZIP dell'anno (skip se già presente)."""
    zippath = REPO / f"{year}Tutto.zip"
    if zippath.exists():
        print(f"✅ {zippath.name} già presente ({zippath.stat().st_size // 1024 // 1024} MB)")
        return zippath

    url = f"{BASE}{year}Tutto.zip"
    print(f"⬇️  Download {url} ...")
    req = urllib.request.Request(url, headers=_HEADERS)
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
    print(f"✅ Scaricato: {zippath.name} ({len(data) / 1024 / 1024:.0f} MB)")
    return zippath


def extract_dati(zippath: pathlib.Path, year: int) -> None:
    """Estrae i file {year}Dati/* in _local/seed/dati/{year}/.

    Gestisce due strutture ZIP della fonte RGS:
    - ``{year}Dati/...`` (root dello zip, anni 2020/2022+)
    - ``{year}Tutto/{year}Dati/...`` (sottocartella, anno 2021)
    """
    out = OUT_DIR / str(year)
    out.mkdir(parents=True, exist_ok=True)

    marker = f"{year}Dati/"
    extracted = 0
    with zipfile.ZipFile(zippath) as z:
        for name in z.namelist():
            if marker not in name:
                continue
            basename = pathlib.Path(name).name
            if not basename:
                continue
            (out / basename).write_bytes(z.read(name))
            extracted += 1

    if extracted == 0:
        print(f"❌ Nessun file {marker}* trovato nello ZIP")
        sys.exit(1)

    print(f"✅ {year}: estratti {extracted} file in {out}")


def apply_fixes(year: int) -> None:
    """Applica i fix per-anno sui file estratti."""
    out = OUT_DIR / str(year)
    for filename, replacements in FIX_2020.items():
        path = out / filename
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        new = text
        for old, new_val in replacements:
            new = new.replace(old, new_val)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print(f"✅ {year}: fix applicato a {filename}")


def main():
    years = [int(a) for a in sys.argv[1:]] or [2024]
    for year in years:
        print(f"=== {year} ===")
        zippath = download_zip(year)
        extract_dati(zippath, year)
        apply_fixes(year)


if __name__ == "__main__":
    main()
