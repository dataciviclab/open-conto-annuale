"""Retribuzioni — stipendi, trend, confronti territoriali."""

import altair as alt
import pandas as pd
import streamlit as st

from sources import YEARS, fmt_num, fmt_pct, load_mart, load_trend

st.title("💰 Retribuzioni")
st.markdown("Stipendi medi, trend nel tempo e confronti tra territori.")

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

# -- Confronto Nord vs Sud ----------------------------------------------------

st.subheader("🌍 Confronto Nord vs Sud")

try:
    from sources import run_sql
    sql_nord_sud = (
        "SELECT "
        "CASE "
        "WHEN regione_beneficiario IN ('PIEMONTE','LOMBARDIA','VENETO','EMILIA-ROMAGNA',"
        "'LIGURIA','TRENTINO-ALTO ADIGE','FRIULI VENEZIA GIULIA') THEN 'Nord' "
        "WHEN regione_beneficiario IN ('CAMPANIA','PUGLIA','CALABRIA','SICILIA',"
        "'SARDEGNA','BASILICATA','ABRUZZO','MOLISE') THEN 'Sud' "
        "ELSE 'Centro/Isole' "
        "END AS area, "
        "COUNT(DISTINCT istituzione) AS n_enti, "
        "COUNT(*) AS n_dipendenti, "
        "ROUND(SUM(tot_spesa) / COUNT(*), 0) AS stipendio_medio "
        "FROM clean_input "
        "GROUP BY area "
        "ORDER BY stipendio_medio DESC"
    )
    df_geo = run_sql(sql_nord_sud, tuple(YEARS))

    chart_geo = (
        alt.Chart(df_geo)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("stipendio_medio:Q", title="Stipendio medio (EUR/anno)"),
            y=alt.Y("area:N", title="", sort="-x"),
            color=alt.Color(
                "area:N",
                scale=alt.Scale(domain=["Nord", "Centro/Isole", "Sud"], range=["#3b82f6", "#f59e0b", "#ef4444"]),
                legend=None,
            ),
            tooltip=["area", alt.Tooltip("stipendio_medio:Q", format=",.0f"), "n_dipendenti", "n_enti"],
        )
        .properties(height=200)
    )
    st.altair_chart(chart_geo, width="stretch")
except Exception as e:
    st.info(f"Confronto territoriale non disponibile: {e}")

# -- Spesa per comparto -------------------------------------------------------

st.markdown("---")
st.subheader("Spesa totale per comparto")

df_comp = load_mart("composizione_retribuzione", "retribuzioni_entrate", anno)
if not df_comp.empty:
    df_comparti = (
        df_comp.groupby("desc_comparto", as_index=False)
        .agg(totale=("tot_importo", "sum"))
        .sort_values("totale", ascending=False)
        .head(10)
    )
    chart_comp = (
        alt.Chart(df_comparti)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3, color="#8b5cf6")
        .encode(
            x=alt.X("totale:Q", title="Importo totale (EUR)", axis=alt.Axis(format="~s")),
            y=alt.Y("desc_comparto:N", title="", sort="-x"),
            tooltip=["desc_comparto", alt.Tooltip("totale:Q", format=",.0f")],
        )
        .properties(height=300)
    )
    st.altair_chart(chart_comp, width="stretch")

st.caption(f"Dati: Conto Annuale RGS/MEF · {anno} · CC BY 4.0")
