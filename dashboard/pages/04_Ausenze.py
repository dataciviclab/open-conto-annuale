"""Assenze & Flessibilità — Malattia, smart working, contratti."""

import altair as alt
import pandas as pd
import streamlit as st

from sources import YEARS, fmt_num, fmt_pct, load_mart, load_trend

st.title("🏥 Assenze & Flessibilità")
st.markdown("Assenze per genere, contratti flessibili e modalità di lavoro.")

anno = st.selectbox("Anno", YEARS, index=len(YEARS) - 1, key="ass_anno")

df_ass = load_mart("assenze", "mart_sintesi", anno)
df_fless = load_mart("flessibili", "mart_sintesi", anno)
df_modalita = load_mart("modalita_flessibile", "mart_sintesi", anno)

# ── Assenze per comparto ──────────────────────────────────────────────────

st.subheader("Assenze per comparto e genere")

df_ass_sorted = df_ass.sort_values("tot_assenze", ascending=False).head(10)
df_ass_melted = df_ass_sorted[["desc_comparto", "tot_assenze_uomini", "tot_assenze_donne"]].melt(
    id_vars="desc_comparto", var_name="genere", value_name="assenze"
)
df_ass_melted["genere"] = df_ass_melted["genere"].map({"tot_assenze_uomini": "Uomini", "tot_assenze_donne": "Donne"})

chart_ass = (
    alt.Chart(df_ass_melted)
    .mark_bar()
    .encode(
        x=alt.X("assenze:Q", title="N. assenze"),
        y=alt.Y("desc_comparto:N", title="", sort="-x"),
        color=alt.Color("genere:N", scale=alt.Scale(domain=["Donne", "Uomini"], range=["#ec4899", "#3b82f6"])),
        tooltip=["desc_comparto", "genere", alt.Tooltip("assenze:Q", format=",.0f")],
    )
    .properties(height=350)
)
st.altair_chart(chart_ass, width="stretch")

st.markdown("---")

# ── Trend assenze ─────────────────────────────────────────────────────────

col_trend, col_fl = st.columns(2)

with col_trend:
    st.subheader("📈 Trend assenze")
    df_trend_ass = load_trend("assenze")
    if not df_trend_ass.empty:
        chart_trend = (
            alt.Chart(df_trend_ass)
            .mark_line(point=True, strokeWidth=2)
            .encode(
                x=alt.X("desc_comparto:N", title=""),
                y=alt.Y("delta_tot_assenze:Q", title="Variazione assenze"),
                color=alt.Color("desc_comparto:N", legend=None),
                tooltip=["desc_comparto", "delta_tot_assenze", "variazione_pct"],
            )
            .properties(height=300)
        )
        st.altair_chart(chart_trend, width="stretch")

with col_fl:
    st.subheader("Contratti flessibili per comparto")
    df_fless_sorted = df_fless.sort_values("tot_flessibili", ascending=False).head(10)
    chart_fl = (
        alt.Chart(df_fless_sorted)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3, color="#f97316")
        .encode(
            x=alt.X("tot_flessibili:Q", title="Dipendenti flessibili", axis=alt.Axis(format="~s")),
            y=alt.Y("desc_comparto:N", title="", sort="-x"),
            tooltip=["desc_comparto", alt.Tooltip("tot_flessibili:Q", format=",.0f")],
        )
        .properties(height=300)
    )
    st.altair_chart(chart_fl, width="stretch")

st.markdown("---")

# ── Dettaglio assenze ─────────────────────────────────────────────────────

st.subheader("Dettaglio assenze per comparto")
display = df_ass[["desc_comparto", "tot_assenze", "tot_assenze_uomini", "tot_assenze_donne", "pct_assenze_donne"]].copy()
display.columns = ["Comparto", "Totale", "Uomini", "Donne", "% Donne"]
display = display.sort_values("Totale", ascending=False)

st.dataframe(
    display.reset_index(drop=True),
    use_container_width=True,
    height=min(400, 40 + len(display) * 40),
    column_config={
        "Comparto": st.column_config.TextColumn("Comparto", width="large"),
        "Totale": st.column_config.NumberColumn("Totale", format="%.0f"),
        "Uomini": st.column_config.NumberColumn("Uomini", format="%.0f"),
        "Donne": st.column_config.NumberColumn("Donne", format="%.0f"),
        "% Donne": st.column_config.NumberColumn("% Donne", format="%.1f"),
    },
)

st.caption(f"Dati: Conto Annuale RGS/MEF · {anno} · CC BY 4.0")
