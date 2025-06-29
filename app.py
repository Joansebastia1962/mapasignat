import streamlit as st
import pandas as pd
import plotly.express as px

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQa0MVPhnDx4MXxizywIfSOazaFUreIbwKmUfVh1ZpYIDlbZT2jtRroAY5vT-7Ca2SJNVZuP6GOlFej/pub?output=csv"

@st.cache_data
def carregar_dades():
    df = pd.read_csv(URL)
    df["Signatures_num"] = df["Signatures(%)"].str.replace('%', '').astype(float)
    df["Signatures_normalized"] = df["Signatures_num"] / 100
    return df

df = carregar_dades()

st.title("Distribució Docents i Signatures - Jerarquia Completa")

fig = px.treemap(
    df,
    names="ID",
    parents="patern",
    values="Professorat",
    color="Signatures_normalized",
    color_continuous_scale=["#ffffff", "#00aa00"],
    hover_data={"Professorat": True, "Signatures(%)": True, "Signatures_normalized": False}
)

fig.update_traces(root_color="lightgrey")
fig.update_layout(margin=dict(t=30, l=0, r=0, b=0))

st.plotly_chart(fig, use_container_width=True)

if st.button("🔄 Refresca dades"):
    st.cache_data.clear()
    st.rerun()