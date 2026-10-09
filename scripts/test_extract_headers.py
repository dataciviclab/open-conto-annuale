"""Test pure per la normalizzazione header pre-2017 in scripts/extract_dati.py."""

from __future__ import annotations

import importlib.util
import pathlib
import sys

import pytest

_EXTRACT = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "extract_dati.py"
_spec = importlib.util.spec_from_file_location("extract_dati", _EXTRACT)
assert _spec and _spec.loader
extract_dati = importlib.util.module_from_spec(_spec)
sys.modules["extract_dati"] = extract_dati
_spec.loader.exec_module(extract_dati)


@pytest.mark.pure_unit
def test_style_header_spazi_e_accenti():
    assert extract_dati._style_header("Istituzione") == "ISTITUZIONE"
    assert extract_dati._style_header("Totale Spesa") == "TOTALE_SPESA"
    assert extract_dati._style_header("Indennità Fisse") == "INDENNITA_FISSE"


@pytest.mark.pure_unit
def test_style_header_preserva_percent():
    assert extract_dati._style_header("Part Time Inf50% Uomini") == "PART_TIME_INF50%_UOMINI"
    assert extract_dati._style_header("Part Time Sup50% Donne") == "PART_TIME_SUP50%_DONNE"


@pytest.mark.pure_unit
def test_override_eta_bug_fonte():
    ovr = extract_dati._HEADER_OVERRIDES_PRE2017["ETA"]
    assert ovr["FASCIA_ANZIANITA"] == "Fascia Età"


@pytest.mark.pure_unit
def test_override_comandati_domme_typo_fonte():
    ovr = extract_dati._HEADER_OVERRIDES_PRE2017["COMANDATI_FUORI_RUOLO_ESONERI"]
    assert ovr["COMANDATIDISTACCATIDONNE"] == "COMANDATI_DISTACCATI_DOMME"


@pytest.mark.pure_unit
def test_override_occupazione_part_time_sup(tmp_path):
    csv_path = tmp_path / "OCCUPAZIONE_2015.CSV"
    csv_path.write_text(
        "ISTITUZIONE;CONTRATTO;CATEGORIA;QUALIFICA;"
        "PERSONALE_TEMPO_PIENO_UOMINI;PERSONALE_TEMPO_PIENO_DONNE;"
        "PART_TIME_INF50%_UOMINI;PART_TIME_INF50%_DONNE;"
        "PART_TIMESUP50%_UOMINI;PART_TIME_SUP50%_DONNE\n"
        "C001;MNST;IR;0IR000;1;0;0;1;0;0\n",
        encoding="utf-8",
    )
    # Simula header già stilizzati: riscrittura deve mappare SUP50 senza spazio
    # Partiamo da header raw stilizzati dallo script di estrazione
    csv_path.write_text(
        "ISTITUZIONE;CONTRATTO;CATEGORIA;QUALIFICA;"
        "Personale Tempo Pieno Uomini;Personale Tempo Pieno Donne;"
        "Part Time Inf50% Uomini;Part Time Inf50% Donne;"
        "Part TimeSup50% Uomini;Part Time Sup50% Donne\n"
        "C001;MNST;IR;0IR000;1;0;0;1;0;0\n",
        encoding="utf-8",
    )
    changed = extract_dati._rename_headers_pre2017(csv_path, "OCCUPAZIONE")
    assert changed
    header = csv_path.read_text(encoding="utf-8").split("\n")[0]
    assert "PART_TIME_SUP50%_UOMINI" in header
    assert "PART_TIME_INF50%_UOMINI" in header
    assert "PART_TIMESUP50%" not in header


@pytest.mark.pure_unit
def test_rename_headers_eta_mappa_fascia(tmp_path):
    csv_path = tmp_path / "ETA_2015.CSV"
    csv_path.write_text(
        "ISTITUZIONE;CONTRATTO;CATEGORIA;QUALIFICA;Fascia Anzianità;UOMINI;DONNE\n"
        "C001;MNST;IR;0IR000;E40;10;5\n",
        encoding="utf-8",
    )
    changed = extract_dati._rename_headers_pre2017(csv_path, "ETA")
    assert changed
    header = csv_path.read_text(encoding="utf-8").split("\n")[0]
    assert "Fascia Età" in header
    assert "Fascia Anzianità" not in header


@pytest.mark.pure_unit
def test_rename_headers_idempotente(tmp_path):
    """Seconda esecuzione su header già normalizzati non deve cambiare nulla."""
    csv_path = tmp_path / "ETA_2015.CSV"
    csv_path.write_text(
        "ISTITUZIONE;CONTRATTO;CATEGORIA;QUALIFICA;Fascia Età;UOMINI;DONNE\n"
        "C001;MNST;IR;0IR000;E40;10;5\n",
        encoding="utf-8",
    )
    assert extract_dati._rename_headers_pre2017(csv_path, "ETA") is False
    header = csv_path.read_text(encoding="utf-8").split("\n")[0]
    assert "Fascia Età" in header
    assert "FASCIA_ETA" not in header


@pytest.mark.pure_unit
def test_rename_headers_idempotente_occupazione(tmp_path):
    csv_path = tmp_path / "OCCUPAZIONE_2015.CSV"
    normalized = (
        "ISTITUZIONE;CONTRATTO;CATEGORIA;QUALIFICA;"
        "PERSONALE_TEMPO_PIENO_UOMINI;PERSONALE_TEMPO_PIENO_DONNE;"
        "PART_TIME_INF50%_UOMINI;PART_TIME_INF50%_DONNE;"
        "PART_TIME_SUP50%_UOMINI;PART_TIME_SUP50%_DONNE\n"
    )
    csv_path.write_text(normalized, encoding="utf-8")
    assert extract_dati._rename_headers_pre2017(csv_path, "OCCUPAZIONE") is False
    assert csv_path.read_text(encoding="utf-8").split("\n")[0] == normalized.strip()
