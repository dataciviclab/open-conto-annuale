"""Panoramica PA — KPI, trend, distribuzione geografica, piramide età."""

import altair as alt
import streamlit as st

from sources import YEARS, fmt_eur, fmt_num, fmt_pct, load_mart, load_trend, load_mart_flat

st.title("🏛️ Conto Annuale PA")
st.markdown("**Panoramica** — Il quadro del personale delle pubbliche amministrazioni italiane.")

# ── Filtri ──────────────────────────────────────────────────────────────────

anno = st.selectbox("Anno", YEARS, index=len(YEARS) - 1, key="pan_anno")

# ── Carica dati ─────────────────────────────────────────────────────────────

df_occ = load_mart("occupazione", "mart_sintesi", anno)
df_costo = load_mart("costo_lavoro", "mart_sintesi", anno)
df_ret = load_mart("retribuzione_media", "mart_sintesi", anno)
df_trend = load_trend("occupazione")

# ── KPI ────────────────────────────────────────────────────────────────────

tot_dip = df_occ["tot_dipendenti"].sum()
tot_donne = df_occ["tot_donne"].sum()
pct_donne = tot_donne / tot_dip * 100 if tot_dip else 0
tot_costo = df_costo["tot_spesa"].sum()
n_comparti = df_occ["codi_comparto"].nunique()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Dipendenti", fmt_num(tot_dip))
k2.metric("% Donne", fmt_pct(pct_donne))
k3.metric("Costo lavoro", fmt_eur(tot_costo, compact=True))
k4.metric("Comparti", n_comparti)

st.markdown("---")

# ── Trend occupazione + Costo lavoro ───────────────────────────────────────

col_trend, col_costo = st.columns(2)

with col_trend:
    st.subheader("📈 Variazione occupazione 2017→2024")
    df_trend_sorted = df_trend.sort_values("variazione_pct", ascending=True)
    chart_trend = (
        alt.Chart(df_trend_sorted)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("variazione_pct:Q", title="Variazione %"),
            y=alt.Y("desc_comparto:N", title="", sort="-x"),
            color=alt.Color(
                "variazione_pct:Q",
                scale=alt.Scale(domain=[-2, 0, 8], range=["#ef4444", "#6b7280", "#10b981"]),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("desc_comparto:N", title="Comparto"),
                alt.Tooltip("delta_dipendenti:Q", title="Delta", format=",.0f"),
                alt.Tooltip("variazione_pct:Q", title="Var %", format=".1f"),
            ],
        )
        .properties(height=300)
    )
    st.altair_chart(chart_trend, width="stretch")

with col_costo:
    st.subheader("💰 Costo lavoro per comparto")
    df_costo_sorted = df_costo.sort_values("tot_spesa", ascending=False).head(10)
    chart_costo = (
        alt.Chart(df_costo_sorted)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, color="#f59e0b")
        .encode(
            x=alt.X("tot_spesa:Q", title="Spesa (€)", axis=alt.Axis(format="~s")),
            y=alt.Y("desc_comparto:N", title="", sort="-x"),
            tooltip=[
                alt.Tooltip("desc_comparto:N", title="Comparto"),
                alt.Tooltip("tot_spesa:Q", title="Spesa", format=",.0f"),
            ],
        )
        .properties(height=300)
    )
    st.altair_chart(chart_costo, width="stretch")

st.markdown("---")

# ── Distribuzione geografica ───────────────────────────────────────────────

st.subheader("🗺️ Distribuzione per regione")

df_geo = load_mart_flat("distribuzione", "distribuzione_italia")
df_geo_year = df_geo[df_geo["anno"] == anno].copy()

if not df_geo_year.empty:
    # Aggrega per regione (somma tutti i comparti)
    df_regioni = (
        df_geo_year.groupby("regione")
        .agg(tot_dipendenti=("tot_dipendenti", "sum"), tot_donne=("tot_donne", "sum"))
        .reset_index()
    )
    df_regioni["pct_donne"] = (df_regioni["tot_donne"] / df_regioni["tot_dipendenti"] * 100).round(1)
    df_regioni = df_regioni.sort_values("tot_dipendenti", ascending=True)

    chart_geo = (
        alt.Chart(df_regioni)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("tot_dipendenti:Q", title="Dipendenti", axis=alt.Axis(format="~s")),
            y=alt.Y("regione:N", title="", sort="-x"),
            color=alt.Color(
                "pct_donne:Q",
                scale=alt.Scale(scheme="blues"),
                title="% Donne",
            ),
            tooltip=[
                alt.Tooltip("regione:N", title="Regione"),
                alt.Tooltip("tot_dipendenti:Q", title="Dipendenti", format=",.0f"),
                alt.Tooltip("pct_donne:Q", title="% Donne", format=".1f"),
            ],
        )
        .properties(height=400)
    )
    st.altair_chart(chart_geo, width="stretch")
else:
    st.info("Dati geografici non disponibili per questo anno.")

st.markdown("---")

# ── Piramide età ──────────────────────────────────────────────────────────

st.subheader("👥 Piramide età del personale PA")

df_eta = load_mart_flat("personale", "personale_eta_italia")
df_eta_year = df_eta[df_eta["anno"] == anno].copy()

if not df_eta_year.empty:
    # Prepara dati per piramide: uomini positivi, donne negative
    df_piramide = df_eta_year[["fascia", "tot_uomini", "tot_donne"]].copy()
    df_piramide = df_piramide.sort_values("fascia")
    df_piramide["uomini"] = df_piramide["tot_uomini"]
    df_piramide["donne"] = -df_piramide["tot_donne"]

    df_melted = df_piramide.melt(id_vars="fascia", value_vars=["uomini", "donne"], var_name="genere", value_name="dipendenti")

    chart_piramide = (
        alt.Chart(df_melted)
        .mark_bar(cornerRadiusTopLeft=2, cornerRadiusTopRight=2)
        .encode(
            x=alt.X("dipendenti:Q", title="Dipendenti", axis=alt.Axis(format="~s", labelExpr="abs(datum.value)")),
            y=alt.Y("fascia:N", title="Fascia età", sort="ascending"),
            color=alt.Color(
                "genere:N",
                scale=alt.Scale(domain=["uomini", "donne"], range=["#3b82f6", "#ec4899"]),
                title="Genere",
            ),
            tooltip=[
                alt.Tooltip("fascia:N", title="Fascia"),
                alt.Tooltip("genere:N", title="Genere"),
                alt.Tooltip("dipendenti:Q", title="Dipendenti", format=",.0f"),
            ],
        )
        .properties(height=350)
    )
    st.altair_chart(chart_piramide, width="stretch")
else:
    st.info("Dati anagrafici non disponibili per questo anno.")

st.caption(f"Dati: Conto Annuale RGS/MEF · {anno} · CC BY 4.0")
