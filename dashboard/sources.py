"""Fonti dati per la dashboard Conto Annuale PA.

Layer sottile che wrappa ``lab_connectors.duckdb.queries`` con
``@st.cache_data`` per Streamlit. Tutta la logica di risoluzione
path GCS e DuckDB sta in lab-connectors — qui solo la cache.
"""

from __future__ import annotations

import streamlit as st

from lab_connectors.duckdb.queries import (
    load_mart_table as _load_mart_table,
    load_mart_flat as _load_mart_flat,
    query_clean as _query_clean,
    count_rows as _count_rows,
    years_from_registry,
)
from lab_connectors.formatters import fmt_eur, fmt_num, fmt_pct
from lab_connectors.registry import load_registry
from pathlib import Path

# ── Costanti dominio ────────────────────────────────────────────────────────

PREFIX = "conto-annuale/"
SLUG = "conto_annuale"

_registry = load_registry(Path(__file__).parent.parent / "registry" / "registry.json")
_all_years = years_from_registry(_registry)
YEARS = list(range(min(_all_years), max(_all_years) + 1)) if _all_years else [2020, 2021, 2022, 2023, 2024]

# ── Cached wrappers ─────────────────────────────────────────────────────────


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart(slug: str, table: str, year: int):
    """Carica un singolo mart table da GCS (cached 1h)."""
    return _load_mart_table(slug, table, year, prefix=PREFIX)


@st.cache_data(ttl=3600, show_spinner=False)
def load_trend(slug: str):
    """Carica il mart_trend multi-anno (cached 1h)."""
    return _load_mart_flat(slug, "mart_trend", prefix=PREFIX)


@st.cache_data(ttl=3600, show_spinner=False)
def get_row_count(slug: str, year: int):
    """Conta righe clean per un anno (cached 1h)."""
    return _count_rows(slug, year, prefix=PREFIX)


@st.cache_data(ttl=3600, show_spinner=False)
def run_sql(sql: str, years: tuple[int, ...] = tuple(YEARS)):
    """Esegue SQL sul clean layer (cached 1h)."""
    return _query_clean(SLUG, sql, list(years), prefix=PREFIX)
