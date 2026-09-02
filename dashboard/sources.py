"""Fonti dati per la dashboard Conto Annuale PA.

Layer sottile che wrappa ``lab_connectors.duckdb.queries`` con
``@st.cache_data`` per Streamlit. Tutta la logica di risoluzione
path e auto-detect locale/GCS sta in lab-connectors.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from lab_connectors.duckdb.queries import (
    count_rows as _count_rows,
    load_mart_flat as _load_mart_flat,
    load_mart_table as _load_mart_table,
    query_clean as _query_clean,
    years_from_registry,
)
from lab_connectors.formatters import fmt_eur, fmt_num, fmt_pct
from lab_connectors.registry import load_registry

# ── Costanti dominio ────────────────────────────────────────────────────────

PREFIX = "conto-annuale/"
SLUG = "conto_annuale"

_REPO = Path(__file__).parent.parent

# Rileva locale per il prefix (GCS usa "conto-annuale/", locale no)
_LOCAL = (_REPO / "out" / "data").is_dir()
_PREFIX = "" if _LOCAL else PREFIX

# ── Anni disponibili ───────────────────────────────────────────────────────

_registry = load_registry(_REPO / "registry" / "registry.json")
_all_years = years_from_registry(_registry)
YEARS = list(range(min(_all_years), max(_all_years) + 1)) if _all_years else []


# ── Cached wrappers ─────────────────────────────────────────────────────────


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart(slug: str, table: str, year: int):
    """Carica un singolo mart table (cached 1h). Auto-detect locale/GCS."""
    return _load_mart_table(slug, table, year, prefix=_PREFIX)


@st.cache_data(ttl=3600, show_spinner=False)
def load_trend(slug: str):
    """Carica il mart_trend multi-anno (cached 1h)."""
    return _load_mart_flat(slug, "mart_trend", prefix=_PREFIX)


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart_flat(slug: str, table: str):
    """Carica un mart multi-anno (cached 1h)."""
    return _load_mart_flat(slug, table, prefix=_PREFIX)


@st.cache_data(ttl=3600, show_spinner=False)
def get_row_count(slug: str, year: int):
    """Conta righe clean per un anno (cached 1h)."""
    return _count_rows(slug, year, prefix=_PREFIX)


@st.cache_data(ttl=3600, show_spinner=False)
def run_sql(sql: str, years: tuple[int, ...] = tuple(YEARS)):
    """Esegue SQL sul clean layer (cached 1h)."""
    return _query_clean(SLUG, sql, list(years), prefix=_PREFIX)
