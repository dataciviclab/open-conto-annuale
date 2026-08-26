"""Retribuzioni — Stipendi, composizione, confronti."""

import altair as alt
import pandas as pd
import streamlit as st

from sources import YEARS, fmt_eur, fmt_num, load_mart

st.title("💰 Retribuzioni")
st.markdown("Stipendi medi, composizione e confronti tra comparti.")

anno = st.selectbox("Anno", YEARS, index=len(YEARS) - 1, key="ret_anno")

df_ret = load_mart("retribuzione_media", "mart_sintesi", anno)
df_comp = load_mart("composizione_retribuzione", "mart_sintesi", anno)

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
        # Raggruppa per voce e somma
        voci = [c for c in df_comp.columns if c.startswith("avg_")]
        if voci:
            df_voci = df_comp[["desc_comparto"] + voci].copy()
            # Prendi top 6 comparti
            top_comparti = df_ret.nlargest(6, "avg_stipendio")["desc_comparto"].tolist()
            df_voci = df_voci[df_voci["desc_comparto"].isin(top_comparti)]
            df_melted = df_voci.melt(id_vars="desc_comparto", var_name="voce", value_name="importo")
            df_melted["voce"] = df_melted["voce"].str.replace("avg_", "").str.replace("_", " ").str.title()

            chart_comp = (
                alt.Chart(df_melted)
                .mark_bar()
                .encode(
                    x=alt.X("desc_comparto:N", title="", sort="-y"),
                    y=alt.Y("importo:Q", title="€/anno", stack="normalize", axis=alt.Axis(format="%")),
                    color=alt.Color("voce:N", title="Voce"),
                    tooltip=["desc_comparto", "voce", alt.Tooltip("importo:Q", format=",.0f")],
                )
                .properties(height=350)
            )
            st.altair_chart(chart_comp, width="stretch")
    else:
        st.info("Dati composizione non disponibili per questo anno.")

with col_confronto:
    st.subheader("Confronto voci retributive")
    if not df_comp.empty:
        # Media per voce (tutti i comparti)
        media_voci = df_comp[voci].mean()
        media_df = pd.DataFrame({"voce": [v.replace("avg_", "").replace("_", " ").title() for v in voci], "media": media_voci.values})
        media_df = media_df.sort_values("media", ascending=False)

        chart_voci = (
            alt.Chart(media_df)
            .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3, color="#10b981")
            .encode(
                x=alt.X("media:Q", title="Media €/anno"),
                y=alt.Y("voce:N", title="", sort="-x"),
                tooltip=["voce", alt.Tooltip("media:Q", format=",.0f")],
            )
            .properties(height=350)
        )
        st.altair_chart(chart_voci, width="stretch")

st.caption(f"Dati: Conto Annuale RGS/MEF · {anno} · CC BY 4.0")
