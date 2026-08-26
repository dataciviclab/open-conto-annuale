"""Smoke test — verifica che tutte le pagine si importano senza errori."""

from __future__ import annotations

import importlib

import pytest

pytestmark = pytest.mark.smoke

PAGES = [
    "pages.01_Panoramica",
    "pages.02_Occupazione",
    "pages.03_Retribuzioni",
    "pages.04_Ausenze",
]


@pytest.mark.parametrize("module", PAGES)
def test_page_imports(module: str) -> None:
    """Ogni pagina deve importarsi senza errori."""
    importlib.import_module(module)
