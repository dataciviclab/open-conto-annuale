"""Organizzazione PA — titoli di studio, anzianità, comandati."""

import altair as alt
import streamlit as st

from sources import YEARS, fmt_num, fmt_pct, load_mart

st.title("📋 Organizzazione PA")
st.markdown("Titoli di studio, anzianità di servizio e personale comandato — com'è fatta la PA italiana.")

anno = st.selectbox("Anno", YEARS, index=len(YEARS) - 1, key="org_anno")

# ── Titoli di studio ───────────────────────────────────────────────────────

st.subheader("🎓 Titoli di studio del personale")

df_titoli = load_mart("titoli_studio", "titoli_studio_comparti", anno)

if not df_titoli.empty:
    # Aggrega per titolo di studio (tutti i comparti)
    df_titoli_agg = (
        df_titoli.groupby("titolo_studio")
        .agg(tot_uomini=("tot_uomini", "sum"), tot_donne=("tot_donne", "sum"), enti=("enti", "sum"))
        .reset_index()
    )
    df_titoli_agg["totale"] = df_titoli_agg["tot_uomini"] + df_titoli_agg["tot_donne"]
    df_titoli_agg["pct_donne"] = (df_titoli_agg["tot_donne"] / df_titoli_agg["totale"] * 100).round(1)
    df_titoli_agg = df_titoli_agg.sort_values("totale", ascending=True)

    # KPI
    tot = df_titoli_agg["totale"].sum()
    laurea = df_titoli_agg[df_titoli_agg["titolo_studio"].str.contains("LAUREA|Master|Dottorato", case=False, na=False)]["totale"].sum()
    pct_laurea = laurea / tot * 100 if tot else 0

    k1, k2 = st.columns(2)
    k1.metric("Dipendenti totali", fmt_num(tot))
    k2.metric("% con Laurea+", fmt_pct(pct_laurea))

    chart_titoli = (
        alt.Chart(df_titoli_agg)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("totale:Q", title="Dipendenti", axis=alt.Axis(format="~s")),
            y=alt.Y("titolo_studio:N", title="", sort="-x"),
            color=alt.Color(
                "pct_donne:Q",
                scale=alt.Scale(scheme="blues"),
                title="% Donne",
            ),
            tooltip=[
                alt.Tooltip("titolo_studio:N", title="Titolo"),
                alt.Tooltip("totale:Q", title="Totale", format=",.0f"),
                alt.Tooltip("pct_donne:Q", title="% Donne", format=".1f"),
            ],
        )
        .properties(height=300)
    )
    st.altair_chart(chart_titoli, width="stretch")

st.markdown("---")

# ── Anzianità di servizio ──────────────────────────────────────────────────

st.subheader("⏳ Anzianità di servizio")

df_anz = load_mart("anzianita", "anzianita_comparti", anno)

if not df_anz.empty:
    # Aggrega per fascia di anzianità (tutti i comparti)
    df_anz_agg = (
        df_anz.groupby("fascia")
        .agg(tot_uomini=("tot_uomini", "sum"), tot_donne=("tot_donne", "sum"))
        .reset_index()
    )
    df_anz_agg["totale"] = df_anz_agg["tot_uomini"] + df_anz_agg["tot_donne"]
    df_anz_agg["pct_donne"] = (df_anz_agg["tot_donne"] / df_anz_agg["totale"] * 100).round(1)
    df_anz_agg = df_anz_agg.sort_values("fascia")

    # Piramide anzianità
    df_pira = df_anz_agg[["fascia", "tot_uomini", "tot_donne"]].copy()
    df_pira["uomini"] = df_pira["tot_uomini"]
    df_pira["donne"] = -df_pira["tot_donne"]
    df_melted = df_pira.melt(id_vars="fascia", value_vars=["uomini", "donne"], var_name="genere", value_name="dipendenti")

    chart_anz = (
        alt.Chart(df_melted)
        .mark_bar(cornerRadiusTopLeft=2, cornerRadiusTopRight=2)
        .encode(
            x=alt.X("dipendenti:Q", title="Dipendenti", axis=alt.Axis(format="~s", labelExpr="abs(datum.value)")),
            y=alt.Y("fascia:N", title="Fascia anzianità", sort="ascending"),
            color=alt.Color(
                "genere:N",
                scale=alt.Scale(domain=["uomini", "donne"], range=["#3b82f6", "#ec4899"]),
                title="Genere",
            ),
            tooltip=["fascia", "genere", alt.Tooltip("dipendenti:Q", format=",.0f")],
        )
        .properties(height=300)
    )
    st.altair_chart(chart_anz, width="stretch")

st.markdown("---")

# ── Comandati e fuori ruolo ───────────────────────────────────────────────

st.subheader("🔄 Personale comandato e fuori ruolo")

df_com = load_mart("comandati", "mart_sintesi", anno)

if not df_com.empty:
    df_com_sorted = df_com.sort_values("tot_comandati", ascending=False)

    # KPI
    tot_comandati = df_com["tot_comandati"].sum()
    k1, k2 = st.columns(2)
    k1.metric("Comandati/distaccati", fmt_num(tot_comandati))

    chart_com = (
        alt.Chart(df_com_sorted)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3, color="#f97316")
        .encode(
            x=alt.X("tot_comandati:Q", title="Comandati/distaccati", axis=alt.Axis(format="~s")),
            y=alt.Y("desc_comparto:N", title="", sort="-x"),
            tooltip=[
                alt.Tooltip("desc_comparto:N", title="Comparto"),
                alt.Tooltip("tot_comandati:Q", title="Comandati", format=",.0f"),
                alt.Tooltip("pct_donne:Q", title="% Donne", format=".1f"),
            ],
        )
        .properties(height=300)
    )
    st.altair_chart(chart_com, width="stretch")

st.caption(f"Dati: Conto Annuale RGS/MEF · {anno} · CC BY 4.0")
