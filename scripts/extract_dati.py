#!/usr/bin/env python3
"""Scarica e estrae i dati del Conto Annuale per un dato anno.

1. Scarica lo ZIP ``{year}Tutto.zip`` dal sito RGS.
2. Estrae SOLO i file di ``{year}Dati/`` in ``_local/seed/dati/{year}/``.
3. Normalizza i CSV: delimitatore virgola → punto e virgola,
   encoding Latin-1 → UTF-8. Per gli anni >= 2017 i nomi delle colonne
   restano INTATTI; per year < 2017 gli header vengono riscritti allo
   schema 2017+ (UPPER_SNAKE + override per bug fonte — vedi
   ``_HEADER_OVERRIDES_PRE2017``).
4. Applica il fix PIEDO → PIENO (colonna OCCUPAZIONE, anni 2017-2024).
"""

import csv
import io
import pathlib
import re
import sys
import zipfile

REPO = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://contoannuale.rgs.mef.gov.it/ext/CSV/"
OUT_DIR = REPO / "_local" / "seed" / "dati"

COLUMN_FIXES = {
    "PERSONALE_TEMPO_PIEDO_DONNE": "PERSONALE_TEMPO_PIENO_DONNE",
}

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://contoannuale.rgs.mef.gov.it/web/sicosito/download",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "it-IT,it;q=0.9",
}


def download_zip(year: int) -> pathlib.Path:
    zippath = REPO / f"{year}Tutto.zip"
    if zippath.exists():
        print(f"  {zippath.name} gia' presente ({zippath.stat().st_size // 1024 // 1024} MB)")
        return zippath

    url = f"{BASE}{year}Tutto.zip"
    print(f"  Download {url} ...")
    try:
        from lab_connectors.http import HttpClient

        with HttpClient(timeout=180) as client:
            result = client.get(url, headers=_HEADERS)
        if not result.is_ok or result.response is None:
            print(f"  Download fallito: {result.err or result.response}")
            sys.exit(1)
        data = result.response.content
    except Exception as e:
        print(f"  Download fallito: {e}")
        sys.exit(1)

    if len(data) < 10000:
        print(f"  Download troppo piccolo ({len(data)} bytes)")
        sys.exit(1)

    zippath.write_bytes(data)
    print(f"  Scaricato: {zippath.name} ({len(data) / 1024 / 1024:.0f} MB)")
    return zippath


def _extract_from_zip(z: zipfile.ZipFile, year: int, out: pathlib.Path) -> int:
    marker = f"{year}Dati/"
    extracted = 0
    for name in z.namelist():
        if marker not in name:
            continue
        basename = pathlib.Path(name).name
        if not basename:
            continue
        (out / basename).write_bytes(z.read(name))
        extracted += 1
    return extracted


def extract_dati(zippath: pathlib.Path, year: int) -> None:
    out = OUT_DIR / str(year)
    out.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zippath) as z:
        nested_name = f"{year}Dati.zip"
        if nested_name in z.namelist():
            nested_data = z.read(nested_name)
            with zipfile.ZipFile(io.BytesIO(nested_data)) as nz:
                extracted = _extract_from_zip(nz, year, out)
            if extracted == 0:
                print(f"  Nessun file {year}Dati/* trovato nel sotto-ZIP")
                sys.exit(1)
            print(f"  {year}: estratti {extracted} file da sotto-ZIP in {out}")
            return

        extracted = _extract_from_zip(z, year, out)

    if extracted == 0:
        print(f"  Nessun file {year}Dati/* trovato nello ZIP")
        sys.exit(1)

    print(f"  {year}: estratti {extracted} file in {out}")


def normalize_csv(path: pathlib.Path) -> None:
    """Normalizza un CSV: delimitatore virgola → punto e virgola,
    encoding Latin-1 → UTF-8. Intestazioni INTATTE."""
    try:
        raw = path.read_bytes()
    except Exception:
        return

    text = None
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            text = raw.decode(enc)
            if text.startswith('"') or ";" in text.split("\n")[0]:
                break
        except (UnicodeDecodeError, UnicodeError):
            continue
    if text is None:
        return

    first_line = text.split("\n")[0]
    has_quotes = text.startswith('"')
    has_comma = "," in first_line and ";" not in first_line

    # CSV con punto e virgola e senza virgolette: riscrivi solo se encoding non-UTF-8
    if not has_quotes and not has_comma:
        try:
            raw.decode("utf-8")
            return
        except UnicodeDecodeError:
            path.write_text(text, encoding="utf-8")
            return

    # CSV con virgolette + virgola (pre-2017): riscrivi con ; senza virgolette
    if has_quotes and has_comma:
        reader = csv.DictReader(io.StringIO(text))
        if not reader.fieldnames:
            return

        fieldnames = [fn.strip() for fn in reader.fieldnames]

        out = io.StringIO()
        writer = csv.DictWriter(
            out, fieldnames=fieldnames, delimiter=";", quoting=csv.QUOTE_MINIMAL
        )
        writer.writeheader()

        for row in reader:
            new_row = {}
            for key, val in row.items():
                if key is None:
                    continue
                new_row[key.strip()] = val if val else ""
            writer.writerow(new_row)

        path.write_text(out.getvalue(), encoding="utf-8")


def _style_header(h: str) -> str:
    """Title Case + spazi (pre-2017) → UPPER_SNAKE compatibile col schema 2017+.

    Mantiene ``%`` (es. PART_TIME_INF50%_UOMINI). Accenti → ASCII.
    """
    h = h.strip().replace("%", "\x00")
    for a, b in (
        ("à", "a"),
        ("è", "e"),
        ("é", "e"),
        ("ì", "i"),
        ("ò", "o"),
        ("ù", "u"),
        ("À", "A"),
        ("È", "E"),
        ("É", "E"),
        ("Ì", "I"),
        ("Ò", "O"),
        ("Ù", "U"),
    ):
        h = h.replace(a, b)
    h = re.sub(r"[^A-Za-z0-9\x00]+", "_", h).strip("_").upper()
    return h.replace("\x00", "%")


# Rename espliciti pre-2017 → header 2017 (dopo _style_header).
# Chiavi = nome stilizzato del pre-2017; valori = header esatto 2017
# (i clean.sql dipendono da questi nomi, typo fonte inclusi).
_HEADER_OVERRIDES_PRE2017 = {
    "ETA": {
        # Bug fonte 2015/2016: header "Fascia Anzianità", valori = fasce età (E*)
        "FASCIA_ANZIANITA": "Fascia Età",
    },
    "ETA_MEDIA": {
        "FASCIA_ANZIANITA": "Fascia Età",
    },
    "COSTO_LAVORO": {
        "VOCE_DI_SPESA": "VOCE_SPESA",
    },
    "COMANDATI_FUORI_RUOLO_ESONERI": {
        # 2015/2016: spelling corretto; 2017+ typo DOMME (usato dai clean.sql)
        "COMANDATIDISTACCATIDONNE": "COMANDATI_DISTACCATI_DOMME",
        # 2015/2016: "Esoneri Interno 70%" ≠ 2017 "Aspettative" — non mappare
        # la semantica; solo normalizzazione stile per evitare spazi/% nei nomi.
        "ESONERI_INTERNO_70%_UOMINI": "ESONERI_INTERNO_70_UOMINI",
        "ESONERI_INTERNO_70%_DONNE": "ESONERI_INTERNO_70_DONNE",
    },
    "OCCUPAZIONE": {
        # 2015: "Part TimeSup50%" senza spazio → stile sbagliato
        "PART_TIMESUP50%_UOMINI": "PART_TIME_SUP50%_UOMINI",
        "PART_TIMESUP50%_DONNE": "PART_TIME_SUP50%_DONNE",
    },
    "MODALITA_LAVORO_FLESSIBILE": {
        # Typo fonte 2015/2016: "Soggeti" → "Soggetti"
        "SOGGETI_REPERIBILITA_UOMINI": "SOGGETTI_REPERIBILITA_UOMINI",
        "SOGGETI_REPERIBILITA_DONNE": "SOGGETTI_REPERIBILITA_DONNE",
    },
}


def _rename_headers_pre2017(csv_path: pathlib.Path, table: str) -> bool:
    """Riscrive header CSV pre-2017 allo schema 2017+ (UPPER_SNAKE + override).

    Idempotente: una colonna già uguale a un target di override (o già in
    stile UPPER_SNAKE senza override applicabile) resta invariata, così una
    seconda esecuzione sullo stesso file non rompe il match dei clean.sql.
    """
    text = csv_path.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    if not lines or not lines[0].strip():
        return False

    header_line = lines[0]
    bom = ""
    if header_line.startswith("﻿"):
        bom = "﻿"
        header_line = header_line[1:]
    header_line = header_line.rstrip("\r")

    cols = [c.strip() for c in header_line.split(";")]
    overrides = _HEADER_OVERRIDES_PRE2017.get(table, {})
    override_targets = set(overrides.values())
    new_cols = []
    changed = False
    for c in cols:
        if c in override_targets:
            new_c = c
        else:
            styled = _style_header(c)
            new_c = overrides.get(styled, styled)
        if new_c != c:
            changed = True
        new_cols.append(new_c)

    if not changed:
        return False

    lines[0] = bom + ";".join(new_cols)
    csv_path.write_text("\n".join(lines), encoding="utf-8")
    return True


def normalize_csv_files(year: int, out: pathlib.Path) -> None:
    # 1. Rinomina .csv → .CSV
    for csv_path in out.glob("*.csv"):
        target = csv_path.with_suffix(".CSV")
        if csv_path != target:
            csv_path.rename(target)

    # 2. Rinomina TITOLO_STUDIO → TITOLI_STUDIO_DATI (pre-2017)
    old_ts = out / f"TITOLO_STUDIO_{year}.CSV"
    new_ts = out / f"TITOLI_STUDIO_DATI_{year}.CSV"
    if old_ts.exists() and not new_ts.exists():
        old_ts.rename(new_ts)
        print(f"  {year}: rinominato TITOLO_STUDIO → TITOLI_STUDIO_DATI")

    # 3. Normalizza delimitatore + encoding per anni con CSV non-standard
    if year <= 2017:
        for csv_path in out.glob("*.CSV"):
            normalize_csv(csv_path)

    # 3b. Pre-2017: riscrivi header allo schema 2017+ (UPPER_SNAKE + fix bug fonte)
    if year < 2017:
        renamed = 0
        for csv_path in sorted(out.glob("*.CSV")):
            m = re.match(rf"(.+?)_{year}\.CSV$", csv_path.name)
            table = m.group(1) if m else csv_path.stem
            if _rename_headers_pre2017(csv_path, table):
                renamed += 1
        if renamed:
            print(f"  {year}: header normalizzati su {renamed} file (schema 2017+)")

    # 4. Aggiungi colonne mancanti per dataset con schema crescente
    _add_missing_columns(year, out)


# Colonne aggiunte nel 2021 che non esistono nei CSV 2017-2020
MISSING_COLUMNS = {
    "MODALITA_LAVORO_FLESSIBILE": {
        2021: [
            "PERS_LAVORO_AGILE_U",
            "PERS_LAVORO_AGILE_D",
            "PERS_COWORKING_U",
            "PERS_COWORKING_D",
        ],
    },
}


def _add_missing_columns(year: int, out: pathlib.Path) -> None:
    """Aggiunge colonne vuote ai CSV per anni che non le hanno."""
    for filename, year_thresholds in MISSING_COLUMNS.items():
        csv_path = out / f"{filename}_{year}.CSV"
        if not csv_path.exists():
            continue

        # Trova le colonne da aggiungere per questo anno
        cols_to_add = []
        for threshold, cols in sorted(year_thresholds.items()):
            if year < threshold:
                cols_to_add.extend(cols)

        if not cols_to_add:
            continue

        # Leggi e riscrivi con colonne aggiunte
        text = csv_path.read_text(encoding="utf-8")
        lines = text.split("\n")
        if not lines:
            continue

        # Aggiungi BOM se presente
        header = lines[0]
        bom = ""
        if header.startswith("\ufeff"):
            bom = "\ufeff"
            header = header[1:]

        new_header = header.rstrip("\r") + ";" + ";".join(cols_to_add)
        new_lines = [bom + new_header]

        for line in lines[1:]:
            if line.strip():
                new_lines.append(line.rstrip("\r") + ";" * len(cols_to_add))

        csv_path.write_text("\n".join(new_lines), encoding="utf-8")
        print(f"  {year}: aggiunte {len(cols_to_add)} colonne a {filename}")


def apply_fixes(year: int) -> None:
    if year < 2017:
        return

    out = OUT_DIR / str(year)
    for csv_path in out.glob("*.CSV"):
        if "OCCUPAZIONE" not in csv_path.name.upper():
            continue
        text = csv_path.read_text(encoding="utf-8", errors="replace")
        new = text
        for old, new_val in COLUMN_FIXES.items():
            new = new.replace(old, new_val)
        if new != text:
            csv_path.write_text(new, encoding="utf-8")
            print(f"  {year}: fix PIEDO applicato a {csv_path.name}")


def main():
    years = [int(a) for a in sys.argv[1:]] or [2024]
    for year in years:
        print(f"=== {year} ===")
        zippath = download_zip(year)
        extract_dati(zippath, year)
        normalize_csv_files(year, OUT_DIR / str(year))
        apply_fixes(year)


if __name__ == "__main__":
    main()
