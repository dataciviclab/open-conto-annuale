#!/usr/bin/env python3
"""
Conto Annuale PA · Dashboard Streamlit
Il personale della PA italiana, aperto e interrogabile.
"""

import streamlit as st

st.set_page_config(
    page_title="Conto Annuale PA · Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

pages = {
    "": [
        st.Page("pages/01_Panoramica.py", title="Panoramica PA", icon="📊", default=True),
    ],
    "Analisi": [
        st.Page("pages/02_Personale.py", title="Personale", icon="👥"),
        st.Page("pages/03_Retribuzioni.py", title="Retribuzioni", icon="💰"),
    ],
}

pg = st.navigation(pages, position="sidebar")

st.sidebar.markdown("---")
st.sidebar.caption("Dati: [Conto Annuale RGS](https://contoaunweb.rgs.mef.gov.it/) · MEF")
st.sidebar.caption("Codice: [dataciviclab/open-conto-annuale](https://github.com/dataciviclab/open-conto-annuale)")
st.sidebar.caption("[DataCivicLab](https://dataciviclab.org/) · CC BY 4.0")

pg.run()
