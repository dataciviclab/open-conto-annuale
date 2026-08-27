"""Query SQL — Interroga direttamente i dati del Conto Annuale PA."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lab_connectors.duckdb.sql_page import render_sql_query
from lab_connectors.registry import load_registry

registry = load_registry(Path(__file__).parent.parent.parent / "registry" / "registry.json")

render_sql_query(
    registry=registry,
    prefix="conto-annuale/",
    default_slug="occupazione",
    title="🧪 Query SQL",
    description="Interroga direttamente i dati del Conto Annuale PA. Scrivi SQL su ``clean_input``.",
)
