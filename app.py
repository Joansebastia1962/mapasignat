
import streamlit as st
import pandas as pd
import plotly.express as px

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSHGPTp7clJ4bIpnlqMJBwaYIHKcini9KHMrqzWGs_svIJh-jQkPGh6WlDn7_IRWVYg38nsDGBfqbxs/pub?output=csv"

@st.cache_data
def carregar_dades():
    df = pd.read_csv(URL)
    df["Signatures_num"] = df["Signatures (%)"].str.replace('%', '').astype(float)
    return df

st.set_page_config(layout="wide", page_title="Treemap Docents")

df = carregar_dades()

# Normalització del color entre 0 i 100 manualment
df["Signatures_normalized"] = df["Signatures_num"] / 100

fig = px.treemap(
    df,
    path=[px.Constant("Catalunya"), "Servei Territorial"],
    values="Docents",
    color="Signatures_normalized",
    color_continuous_scale=px.colors.sequential.Greens,
    hover_data={"Docents": True, "Signatures (%)": True, "Signatures_normalized": False},
)

fig.update_traces(texttemplate=df["Signatures (%)"])
fig.update_layout(
    margin=dict(t=30, l=0, r=0, b=0),
    coloraxis_showscale=False
)

st.title("Distribució dels docents per comarques i signatures recollides")
st.plotly_chart(fig, use_container_width=True)
