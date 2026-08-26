"""Fonti dati per la dashboard Conto Annuale PA.

Layer sottile che wrappa ``lab_connectors.duckdb.queries`` con
``@st.cache_data`` per Streamlit. Tutta la logica di risoluzione
path GCS e DuckDB sta in lab-connectors — qui solo la cache.
"""

from __future__ import annotations

import streamlit as st

from lab_connectors.duckdb.queries import (
    load_mart_table as _load_mart_table,
    load_mart_all_years as _load_mart_all_years,
    query_clean as _query_clean,
    count_rows as _count_rows,
)

# ── Costanti dominio ────────────────────────────────────────────────────────

PREFIX = "conto-annuale/"
SLUG = "conto_annuale"
YEARS = [2020, 2021, 2022, 2023, 2024]

# ── Cached wrappers ─────────────────────────────────────────────────────────


@st.cache_data(ttl=3600, show_spinner=False)
def load_mart(slug: str, table: str, year: int):
    """Carica un singolo mart table da GCS (cached 1h)."""
    return _load_mart_table(slug, table, year, prefix=PREFIX)


@st.cache_data(ttl=3600, show_spinner=False)
def load_trend(slug: str):
    """Carica il mart_trend multi-anno (cached 1h).

    Il trend non è partizionato per anno — sta in {slug}/mart_trend.parquet.
    Costruiamo l'URL manualmente.
    """
    from lab_connectors.gcs.paths import https_url

    # Il pattern mart_parquet richiede year, ma il trend non ce l'ha.
    # Usiamo URL diretto: bucket/slug/mart_trend.parquet
    url = f"https://storage.googleapis.com/dataciviclab-mart/{PREFIX}{slug}/mart_trend.parquet"
    import duckdb

    with duckdb.connect() as con:
        return con.sql(f"SELECT * FROM read_parquet('{url}')").df()


@st.cache_data(ttl=3600, show_spinner=False)
def get_row_count(slug: str, year: int):
    """Conta righe clean per un anno (cached 1h)."""
    return _count_rows(slug, year, prefix=PREFIX)


@st.cache_data(ttl=3600, show_spinner=False)
def run_sql(sql: str, years: tuple[int, ...] = tuple(YEARS)):
    """Esegue SQL sul clean layer (cached 1h)."""
    return _query_clean(SLUG, sql, list(years), prefix=PREFIX)


# ── Formattazione ───────────────────────────────────────────────────────────


def fmt_eur(value: float) -> str:
    if abs(value) >= 1_000_000_000:
        return f"€{value / 1_000_000_000:,.1f} mld"
    if abs(value) >= 1_000_000:
        return f"€{value / 1_000_000:,.1f} M"
    if abs(value) >= 1_000:
        return f"€{value / 1_000:,.0f} K"
    return f"€{value:,.0f}"


def fmt_num(value: float) -> str:
    return f"{value:,.0f}"


def fmt_pct(value: float) -> str:
    return f"{value:.1f}%"
