"""Retribuzioni — stipendi, trend, confronti."""

import altair as alt
import pandas as pd
import streamlit as st

from sources import YEARS, load_mart, load_trend

st.title("💰 Retribuzioni")
st.markdown("Stipendi medi, trend nel tempo e composizione per comparto.")

anno = st.selectbox("Anno", YEARS, index=len(YEARS) - 1, key="ret_anno")

# -- Stipendio medio per dipendente ------------------------------------------

st.subheader("Stipendio medio annuo per dipendente")

df_occ = load_mart("occupazione", "mart_sintesi", anno)
df_costo = load_mart("costo_lavoro", "mart_sintesi", anno)

df_stipendio = pd.merge(
    df_occ[["desc_comparto", "tot_dipendenti"]],
    df_costo[["desc_comparto", "tot_spesa"]],
    on="desc_comparto",
)
df_stipendio["stipendio_medio"] = df_stipendio["tot_spesa"] / df_stipendio["tot_dipendenti"]
df_stipendio = df_stipendio.sort_values("stipendio_medio", ascending=False)

chart_ret = (
    alt.Chart(df_stipendio)
    .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
    .encode(
        x=alt.X("stipendio_medio:Q", title="Stipendio medio (EUR/anno)"),
        y=alt.Y("desc_comparto:N", title="", sort="-x"),
        color=alt.Color("stipendio_medio:Q", scale=alt.Scale(scheme="greens"), legend=None),
        tooltip=[
            alt.Tooltip("desc_comparto:N", title="Comparto"),
            alt.Tooltip("stipendio_medio:Q", title="Stipendio medio", format=",.0f"),
            alt.Tooltip("tot_dipendenti:Q", title="Dipendenti", format=",.0f"),
        ],
    )
    .properties(height=350)
)
st.altair_chart(chart_ret, width="stretch")

st.markdown("---")

# -- Trend costo lavoro -------------------------------------------------------

st.subheader("📈 Trend costo lavoro per comparto")

df_trend_costo = load_trend("costo_lavoro")
if not df_trend_costo.empty:
    df_top = df_trend_costo.sort_values("variazione_pct", ascending=True)
    chart_trend = (
        alt.Chart(df_top)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("variazione_pct:Q", title="Variazione %"),
            y=alt.Y("desc_comparto:N", title="", sort="-x"),
            color=alt.Color(
                "variazione_pct:Q",
                scale=alt.Scale(domain=[-2, 0, 10], range=["#ef4444", "#6b7280", "#10b981"]),
                legend=None,
            ),
            tooltip=["desc_comparto", "delta_spesa", "variazione_pct"],
        )
        .properties(height=280)
    )
    st.altair_chart(chart_trend, width="stretch")

st.markdown("---")

# -- Composizione per comparto ------------------------------------------------

st.subheader("Composizione retribuzione per comparto")

df_comp = load_mart("composizione_retribuzione", "retribuzioni_entrate", anno)
if not df_comp.empty:
    # Prendi top 6 comparti per spesa totale
    top_comparti = (
        df_comp.groupby("desc_comparto")
        .agg(totale=("tot_importo", "sum"))
        .nlargest(6, "totale")
        .index.tolist()
    )
    df_filtered = df_comp[df_comp["desc_comparto"].isin(top_comparti)]

    chart_comp = (
        alt.Chart(df_filtered)
        .mark_bar()
        .encode(
            x=alt.X("desc_comparto:N", title="", sort="-y"),
            y=alt.Y("tot_importo:Q", title="Importo (EUR)", stack="normalize", axis=alt.Axis(format="%")),
            color=alt.Color("desc_voce_spesa:N", title="Voce"),
            tooltip=["desc_comparto", "desc_voce_spesa", alt.Tooltip("tot_importo:Q", format=",.0f")],
        )
        .properties(height=350)
    )
    st.altair_chart(chart_comp, width="stretch")

st.caption(f"Dati: Conto Annuale RGS/MEF · {anno} · CC BY 4.0")
