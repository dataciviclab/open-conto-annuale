#!/usr/bin/env python3
"""
Conto Annuale PA · Dashboard Streamlit
Il personale della PA italiana, aperto e interrogabile.
"""

import streamlit as st
from lab_connectors.branding import apply_branding

st.set_page_config(
    page_title="Conto Annuale PA · Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_branding(
    repo_name="open-conto-annuale", repo_url="https://github.com/dataciviclab/open-conto-annuale"
)

pages = {
    "": [
        st.Page("pages/01_Panoramica.py", title="Panoramica PA", icon="📊", default=True),
    ],
    "Analisi": [
        st.Page("pages/02_Personale.py", title="Personale", icon="👥"),
        st.Page("pages/03_Retribuzioni.py", title="Retribuzioni", icon="💰"),
        st.Page("pages/05_Organizzazione.py", title="Organizzazione", icon="📋"),
        st.Page("pages/06_Innovazione.py", title="Innovazione", icon="🚀"),
    ],
    "Strumenti": [
        st.Page("pages/04_SQL.py", title="Query SQL", icon="🧪"),
    ],
}

pg = st.navigation(pages, position="sidebar")

pg.run()
