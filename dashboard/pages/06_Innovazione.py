"""Innovazione PA — flessibilità, contrattazione, mobilità."""

import altair as alt
import streamlit as st

from sources import YEARS, fmt_num, fmt_eur, load_mart, load_trend

st.title("🚀 Innovazione PA")
st.markdown("Lavoro agile, contrattazione integrativa e mobilità del personale — come cambia la PA.")

anno = st.selectbox("Anno", YEARS, index=len(YEARS) - 1, key="inn_anno")

# ── Modalità flessibili ────────────────────────────────────────────────────

st.subheader("🏠 Modalità di lavoro flessibile")

df_fl = load_mart("modalita_flessibile", "mart_sintesi", anno)

if not df_fl.empty:
    tot = df_fl["tot_modalita"].sum()
    tot_tl = df_fl["tot_telelavoro"].sum()
    tot_agile = df_fl["tot_agile"].sum()
    tot_cowork = df_fl["tot_coworking"].sum()
    tot_turn = df_fl["tot_turnazione"].sum()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Telelavoro", fmt_num(tot_tl))
    k2.metric("Lavoro agile", fmt_num(tot_agile))
    k3.metric("Coworking", fmt_num(tot_cowork))
    k4.metric("Turnazione", fmt_num(tot_turn))

    # Bar chart per comparto
    df_fl_sorted = df_fl.sort_values("tot_modalita", ascending=False)
    df_melted = df_fl_sorted[["desc_comparto", "tot_telelavoro", "tot_agile", "tot_coworking", "tot_turnazione"]].melt(
        id_vars="desc_comparto", var_name="modalita", value_name="dipendenti"
    )
    df_melted["modalita"] = df_melted["modalita"].map({
        "tot_telelavoro": "Telelavoro",
        "tot_agile": "Lavoro agile",
        "tot_coworking": "Coworking",
        "tot_turnazione": "Turnazione",
    })

    chart_fl = (
        alt.Chart(df_melted)
        .mark_bar()
        .encode(
            x=alt.X("dipendenti:Q", title="Dipendenti", stack="normalize", axis=alt.Axis(format="%")),
            y=alt.Y("desc_comparto:N", title="", sort="-x"),
            color=alt.Color("modalita:N", title="Modalità"),
            tooltip=["desc_comparto", "modalita", alt.Tooltip("dipendenti:Q", format=",.0f")],
        )
        .properties(height=300)
    )
    st.altair_chart(chart_fl, width="stretch")

    # Trend flessibilità
    df_trend_fl = load_trend("modalita_flessibile")
    if not df_trend_fl.empty:
        st.subheader("📈 Trend lavoro agile (2017→2024)")
        df_trend_fl_sorted = df_trend_fl.sort_values("variazione_pct", ascending=True)
        chart_trend_fl = (
            alt.Chart(df_trend_fl_sorted)
            .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
            .encode(
                x=alt.X("variazione_pct:Q", title="Variazione %"),
                y=alt.Y("desc_comparto:N", title="", sort="-x"),
                color=alt.Color(
                    "variazione_pct:Q",
                    scale=alt.Scale(domain=[-5, 0, 50], range=["#ef4444", "#6b7280", "#10b981"]),
                    legend=None,
                ),
                tooltip=["desc_comparto", "delta_tot_modalita", "variazione_pct"],
            )
            .properties(height=250)
        )
        st.altair_chart(chart_trend_fl, width="stretch")

st.markdown("---")

# ── Contrattazione integrativa ─────────────────────────────────────────────

st.subheader("💼 Spese di contrattazione integrativa")

df_cont = load_mart("contrattazione", "mart_sintesi", anno)

if not df_cont.empty:
    tot_cont = df_cont["tot_importo"].sum()

    k1 = st.columns(1)[0]
    k1.metric("Spesa totale contrattazione", fmt_eur(tot_cont, compact=True))

    df_cont_sorted = df_cont.sort_values("tot_importo", ascending=False)
    chart_cont = (
        alt.Chart(df_cont_sorted)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3, color="#8b5cf6")
        .encode(
            x=alt.X("tot_importo:Q", title="Importo (€)", axis=alt.Axis(format="~s")),
            y=alt.Y("desc_comparto:N", title="", sort="-x"),
            tooltip=[
                alt.Tooltip("desc_comparto:N", title="Comparto"),
                alt.Tooltip("tot_importo:Q", title="Importo", format=",.0f"),
            ],
        )
        .properties(height=250)
    )
    st.altair_chart(chart_cont, width="stretch")

st.markdown("---")

# ── Passaggi di qualifica ──────────────────────────────────────────────────

st.subheader("📊 Passaggi di qualifica")

df_pass = load_mart("passaggi", "mart_sintesi", anno)

if not df_pass.empty:
    tot_pass = df_pass["tot_passaggi"].sum()

    k1 = st.columns(1)[0]
    k1.metric("Totale passaggi", fmt_num(tot_pass))

    df_pass_sorted = df_pass.sort_values("tot_passaggi", ascending=False)
    chart_pass = (
        alt.Chart(df_pass_sorted)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3, color="#06b6d4")
        .encode(
            x=alt.X("tot_passaggi:Q", title="N. passaggi"),
            y=alt.Y("desc_comparto:N", title="", sort="-x"),
            tooltip=[
                alt.Tooltip("desc_comparto:N", title="Comparto"),
                alt.Tooltip("tot_passaggi:Q", title="Passaggi", format=",.0f"),
            ],
        )
        .properties(height=250)
    )
    st.altair_chart(chart_pass, width="stretch")

st.caption(f"Dati: Conto Annuale RGS/MEF · {anno} · CC BY 4.0")
