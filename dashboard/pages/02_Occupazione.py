"""Occupazione & Costo — Dettaglio per comparto."""

import altair as alt
import pandas as pd
import streamlit as st

from sources import YEARS, fmt_eur, fmt_num, fmt_pct, load_mart, load_trend

st.title("👥 Occupazione & Costo")
st.markdown("Dettaglio dipendenti e spesa per comparto della PA.")

# ── Filtri ──────────────────────────────────────────────────────────────────

anno = st.selectbox("Anno", YEARS, index=len(YEARS) - 1, key="occ_anno")

df_occ = load_mart("occupazione", "mart_sintesi", anno)
df_costo = load_mart("costo_lavoro", "mart_sintesi", anno)
df_flessibili = load_mart("flessibili", "mart_sintesi", anno)

# ── Dettaglio per comparto ─────────────────────────────────────────────────

st.subheader("Dipendenti per comparto")
display = df_occ[["desc_comparto", "tot_dipendenti", "tot_donne", "tot_uomini", "pct_donne", "pct_part_time", "enti"]].copy()
display.columns = ["Comparto", "Dipendenti", "Donne", "Uomini", "% Donne", "% Part-Time", "Enti"]
display = display.sort_values("Dipendenti", ascending=False)

st.dataframe(
    display.reset_index(drop=True),
    use_container_width=True,
    height=min(400, 40 + len(display) * 40),
    column_config={
        "Comparto": st.column_config.TextColumn("Comparto", width="large"),
        "Dipendenti": st.column_config.NumberColumn("Dipendenti", format="%.0f"),
        "Donne": st.column_config.NumberColumn("Donne", format="%.0f"),
        "Uomini": st.column_config.NumberColumn("Uomini", format="%.0f"),
        "% Donne": st.column_config.NumberColumn("% Donne", format="%.1f"),
        "% Part-Time": st.column_config.NumberColumn("% Part-Time", format="%.1f"),
        "Enti": st.column_config.NumberColumn("Enti", format="%.0f"),
    },
)

st.markdown("---")

# ── Part-time per comparto ─────────────────────────────────────────────────

col_pt, col_fl = st.columns(2)

with col_pt:
    st.subheader("Part-Time per comparto")
    df_pt = df_occ.sort_values("pct_part_time", ascending=False).head(10)
    chart_pt = (
        alt.Chart(df_pt)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3, color="#06b6d4")
        .encode(
            x=alt.X("pct_part_time:Q", title="% Part-Time"),
            y=alt.Y("desc_comparto:N", title="", sort="-x"),
            tooltip=[
                alt.Tooltip("desc_comparto:N", title="Comparto"),
                alt.Tooltip("pct_part_time:Q", title="% PT", format=".1f"),
                alt.Tooltip("tot_part_time:Q", title="N. PT", format=",.0f"),
            ],
        )
        .properties(height=280)
    )
    st.altair_chart(chart_pt, width="stretch")

with col_fl:
    st.subheader("Contratti flessibili")
    df_fl = load_mart("flessibili", "mart_sintesi", anno)
    df_fl_sorted = df_fl.sort_values("tot_flessibili", ascending=False).head(10) if "tot_flessibili" in df_fl.columns else df_fl.head(10)
    chart_fl = (
        alt.Chart(df_fl_sorted)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3, color="#f97316")
        .encode(
            x=alt.X("tot_flessibili:Q", title="Dipendenti flessibili", axis=alt.Axis(format="~s")),
            y=alt.Y("desc_comparto:N", title="", sort="-x"),
            tooltip=["desc_comparto", alt.Tooltip("tot_flessibili:Q", format=",.0f")],
        )
        .properties(height=280)
    )
    st.altair_chart(chart_fl, width="stretch")

st.caption(f"Dati: Conto Annuale RGS/MEF · {anno} · CC BY 4.0")
