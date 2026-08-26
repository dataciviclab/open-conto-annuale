"""Panoramica PA — KPI, trend, composizione dipendenti."""

import altair as alt
import pandas as pd
import streamlit as st

from sources import YEARS, fmt_eur, fmt_num, fmt_pct, load_mart, load_trend

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
k3.metric("Costo lavoro", fmt_eur(tot_costo))
k4.metric("Comparti", n_comparti)

st.markdown("---")

# ── Trend occupazione ───────────────────────────────────────────────────────

col_trend, col_costo = st.columns(2)

with col_trend:
    st.subheader("📈 Variazione occupazione 2020→2024")
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
                alt.Tooltip("tot_spesa_milioni:Q", title="Milioni €", format=",.0f"),
            ],
        )
        .properties(height=300)
    )
    st.altair_chart(chart_costo, width="stretch")

st.markdown("---")

# ── Composizione genere ────────────────────────────────────────────────────

col_genere, col_retribuzione = st.columns(2)

with col_genere:
    st.subheader("👫 Composizione per genere")
    df_genere = df_occ[["desc_comparto", "tot_uomini", "tot_donne"]].melt(
        id_vars="desc_comparto", var_name="genere", value_name="dipendenti"
    )
    chart_genere = (
        alt.Chart(df_genere)
        .mark_bar()
        .encode(
            x=alt.X("desc_comparto:N", title="", sort="-y"),
            y=alt.Y("dipendenti:Q", title="Dipendenti", stack="normalize", axis=alt.Axis(format="%")),
            color=alt.Color("genere:N", scale=alt.Scale(domain=["tot_donne", "tot_uomini"], range=["#ec4899", "#3b82f6"])),
            tooltip=["desc_comparto", "genere", alt.Tooltip("dipendenti:Q", format=",.0f")],
        )
        .properties(height=300)
    )
    st.altair_chart(chart_genere, width="stretch")

with col_retribuzione:
    st.subheader("💶 Retribuzione media per comparto")
    df_ret_sorted = df_ret.sort_values("avg_stipendio", ascending=False).head(10)
    chart_ret = (
        alt.Chart(df_ret_sorted)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, color="#8b5cf6")
        .encode(
            x=alt.X("avg_stipendio:Q", title="Stipendio medio (€/anno)"),
            y=alt.Y("desc_comparto:N", title="", sort="-x"),
            tooltip=[
                alt.Tooltip("desc_comparto:N", title="Comparto"),
                alt.Tooltip("avg_stipendio:Q", title="Stipendio", format=",.0f"),
                alt.Tooltip("avg_tredicesima:Q", title="13a", format=",.0f"),
                alt.Tooltip("avg_straordinario:Q", title="Straordinari", format=",.0f"),
            ],
        )
        .properties(height=300)
    )
    st.altair_chart(chart_ret, width="stretch")

st.caption(f"Dati: Conto Annuale RGS/MEF · {anno} · CC BY 4.0")
