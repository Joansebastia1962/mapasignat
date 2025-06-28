import streamlit as st
import pandas as pd
import plotly.express as px

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSHGPTp7clJ4bIpnlqMJBwaYIHKcini9KHMrqzWGs_svIJh-jQkPGh6WlDn7_IRWVYg38nsDGBfqbxs/pub?output=csv"

@st.cache_data
def carregar_dades():
    df = pd.read_csv(URL)
    df["Signatures_num"] = df["Signatures(%)"].str.replace('%', '').astype(float)
    return df

st.set_page_config(layout="wide", page_title="Treemap Docents")

df = carregar_dades()

df["Signatures_normalized"] = df["Signatures_num"] / 100

# Mostra només el % com a text
df["Etiqueta"] = df["Signatures(%)"]

fig = px.treemap(
    df,
    path=[px.Constant("Catalunya"), "Servei Territorial"],
    values="Professorat ",
    color="Signatures_normalized",
    color_continuous_scale=px.colors.sequential.Greens,
    range_color=[0, 1],
    hover_data={
        "Servei Territorial": True,
        "Professorat ": True,
        "Signatures(%)": True,
    }
)

fig.update_traces(textinfo="label+text", text=df["Etiqueta"])

fig.update_layout(
    margin=dict(t=30, l=0, r=0, b=0),
    coloraxis_showscale=False
)

st.title("Distribució dels docents per serveis territorials i signatures recollides")
st.plotly_chart(fig, use_container_width=True)
