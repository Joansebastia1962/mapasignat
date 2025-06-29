
import streamlit as st
import pandas as pd
import plotly.express as px

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQa0MVPhnDx4MXxizywIfSOazaFUreIbwKmUfVh1ZpYIDlbZT2jtRroAY5vT-7Ca2SJNVZuP6GOlFej/pub?gid=136911370&single=true&output=csv"

@st.cache_data
def carregar_dades():
    df = pd.read_csv(URL)
    st.write("Columnes disponibles:", df.columns)  # Verifica les columnes
    df["Signatures_num"] = df["Signatures(%)"].str.replace('%', '').astype(float)
    df["Signatures_normalized"] = df["Signatures_num"] / 100
    return df

df = carregar_dades()

st.set_page_config(layout="wide", page_title="Treemap Docents")

st.title("Distribució Docents i Signatures - Jerarquia Completa")

fig = px.treemap(
    df,
    names="id",
    parents="parent",
    values="Professorat",
    color="Signatures_normalized",
    color_continuous_scale="Greens",
    range_color=[0, 1],
    hover_data={
        "Professorat": True,
        "Signatures(%)": True,
        "Signatures_normalized": False
    }
)

fig.update_traces(
    texttemplate='%{label}<br>%{customdata[1]}',
    textfont_size=18
)

st.plotly_chart(fig, use_container_width=True)

if st.button("🔄 Refresca dades"):
    st.cache_data.clear()
    st.experimental_rerun()
