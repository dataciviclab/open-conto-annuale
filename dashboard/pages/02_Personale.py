"""Personale — occupazione, assenze, flessibilità (unificato)."""

import altair as alt
import pandas as pd
import streamlit as st

from sources import YEARS, fmt_num, fmt_pct, load_mart, load_trend

st.title("👥 Personale PA")
st.markdown("Occupazione, assenze e flessibilità — tutto in una pagina.")

anno = st.selectbox("Anno", YEARS, index=len(YEARS) - 1, key="per_anno")

tab_occ, tab_ass, tab_fl = st.tabs(["Occupazione", "Assenze", "Flessibilità"])

# ── Tab Occupazione ────────────────────────────────────────────────────────

with tab_occ:
    st.subheader("Dipendenti per comparto")
    df_occ = load_mart("occupazione", "mart_sintesi", anno)
    df_trend = load_trend("occupazione")

    # KPI
    tot = df_occ["tot_dipendenti"].sum()
    pct_donne = df_occ["tot_donne"].sum() / tot * 100 if tot else 0
    pct_pt = df_occ["tot_part_time"].sum() / tot * 100 if tot else 0

    k1, k2, k3 = st.columns(3)
    k1.metric("Dipendenti", fmt_num(tot))
    k2.metric("% Donne", fmt_pct(pct_donne))
    k3.metric("% Part-Time", fmt_pct(pct_pt))

    # Tabella
    display = df_occ[["desc_comparto", "tot_dipendenti", "tot_donne", "tot_uomini", "pct_donne", "pct_part_time"]].copy()
    display.columns = ["Comparto", "Dipendenti", "Donne", "Uomini", "% Donne", "% PT"]
    display = display.sort_values("Dipendenti", ascending=False)
    st.dataframe(display, use_container_width=True, height=250)

    # Trend variazione
    st.subheader("Variazione 2020→2024")
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
            tooltip=["desc_comparto", "delta_dipendenti", "variazione_pct"],
        )
        .properties(height=280)
    )
    st.altair_chart(chart_trend, width="stretch")

# ── Tab Assenze ─────────────────────────────────────────────────────────────

with tab_ass:
    df_ass = load_mart("assenze", "mart_sintesi", anno)
    df_trend_ass = load_trend("assenze")

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

    # Trend assenze
    st.subheader("Trend assenze")
    if not df_trend_ass.empty:
        chart_trend_ass = (
            alt.Chart(df_trend_ass)
            .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
            .encode(
                x=alt.X("delta_tot_assenze:Q", title="Variazione assenze"),
                y=alt.Y("desc_comparto:N", title="", sort="-x"),
                color=alt.Color(
                    "delta_tot_assenze:Q",
                    scale=alt.Scale(domain=[-50000, 0, 50000], range=["#10b981", "#6b7280", "#ef4444"]),
                    legend=None,
                ),
                tooltip=["desc_comparto", "delta_tot_assenze", "variazione_pct"],
            )
            .properties(height=280)
        )
        st.altair_chart(chart_trend_ass, width="stretch")

# ── Tab Flessibilità ───────────────────────────────────────────────────────

with tab_fl:
    df_fl = load_mart("flessibili", "mart_sintesi", anno)

    st.subheader("Contratti flessibili per comparto")
    df_fl_sorted = df_fl.sort_values("tot_flessibili", ascending=False).head(10)
    chart_fl = (
        alt.Chart(df_fl_sorted)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3, color="#f97316")
        .encode(
            x=alt.X("tot_flessibili:Q", title="Dipendenti flessibili", axis=alt.Axis(format="~s")),
            y=alt.Y("desc_comparto:N", title="", sort="-x"),
            tooltip=["desc_comparto", alt.Tooltip("tot_flessibili:Q", format=",.0f")],
        )
        .properties(height=350)
    )
    st.altair_chart(chart_fl, width="stretch")

st.caption(f"Dati: Conto Annuale RGS/MEF · {anno} · CC BY 4.0")
