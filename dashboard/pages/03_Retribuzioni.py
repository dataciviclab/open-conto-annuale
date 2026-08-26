"""Retribuzioni — Stipendi, composizione, confronti."""

import altair as alt
import pandas as pd
import streamlit as st

from sources import YEARS, fmt_eur, fmt_num, load_mart

st.title("💰 Retribuzioni")
st.markdown("Stipendi medi, composizione e confronti tra comparti.")

anno = st.selectbox("Anno", YEARS, index=len(YEARS) - 1, key="ret_anno")

df_ret = load_mart("retribuzione_media", "mart_sintesi", anno)
df_comp = load_mart("composizione_retribuzione", "retribuzioni_entrate", anno)

# ── Retribuzione media per comparto ────────────────────────────────────────

st.subheader("Stipendio medio annuo per comparto")
df_ret_sorted = df_ret.sort_values("avg_stipendio", ascending=False)

chart_ret = (
    alt.Chart(df_ret_sorted)
    .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
    .encode(
        x=alt.X("avg_stipendio:Q", title="Stipendio medio (€/anno)"),
        y=alt.Y("desc_comparto:N", title="", sort="-x"),
        color=alt.Color("avg_stipendio:Q", scale=alt.Scale(scheme="greens"), legend=None),
        tooltip=[
            alt.Tooltip("desc_comparto:N", title="Comparto"),
            alt.Tooltip("avg_stipendio:Q", title="Stipendio", format=",.0f"),
            alt.Tooltip("avg_tredicesima:Q", title="13a media", format=",.0f"),
            alt.Tooltip("avg_straordinario:Q", title="Straordinari medi", format=",.0f"),
        ],
    )
    .properties(height=350)
)
st.altair_chart(chart_ret, width="stretch")

st.markdown("---")

# ── Composizione retribuzione ──────────────────────────────────────────────

col_comp, col_confronto = st.columns(2)

with col_comp:
    st.subheader("Composizione retribuzione")
    if not df_comp.empty:
        df_voci = df_comp.sort_values("tot_importo", ascending=False).head(8)
        df_voci["voce"] = df_voci["desc_voce_spesa"].str[:40]

        chart_comp = (
            alt.Chart(df_voci)
            .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3, color="#10b981")
            .encode(
                x=alt.X("tot_importo:Q", title="Importo totale (€)", axis=alt.Axis(format="~s")),
                y=alt.Y("voce:N", title="", sort="-x"),
                tooltip=[
                    alt.Tooltip("desc_voce_spesa:N", title="Voce"),
                    alt.Tooltip("tot_importo:Q", title="Totale", format=",.0f"),
                    alt.Tooltip("enti:N", title="Enti", format=",.0f"),
                ],
            )
            .properties(height=350)
        )
        st.altair_chart(chart_comp, width="stretch")

with col_confronto:
    st.subheader("Confronto voci retributive")
    if not df_comp.empty:
        df_voci = df_comp.sort_values("tot_importo", ascending=False).head(8)
        df_voci["voce"] = df_voci["desc_voce_spesa"].str[:40]

        chart_voci = (
            alt.Chart(df_voci)
            .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3, color="#8b5cf6")
            .encode(
                x=alt.X("tot_importo:Q", title="Importo totale (€)", axis=alt.Axis(format="~s")),
                y=alt.Y("voce:N", title="", sort="-x"),
                tooltip=["voce", alt.Tooltip("tot_importo:Q", format=",.0f")],
            )
            .properties(height=350)
        )
        st.altair_chart(chart_voci, width="stretch")

st.caption(f"Dati: Conto Annuale RGS/MEF · {anno} · CC BY 4.0")
