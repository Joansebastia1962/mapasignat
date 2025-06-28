import streamlit as st
import pandas as pd
import plotly.express as px

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSHGPTp7clJ4bIpnlqMJBwaYIHKcini9KHMrqzWGs_svIJh-jQkPGh6WlDn7_IRWVYg38nsDGBfqbxs/pub?output=csv"

@st.cache_data
def carregar_dades():
    df = pd.read_csv(URL)
    df["Signatures_num"] = df["Signatures(%)"].astype(str).str.replace('%', '').astype(float)
    df["Signatures_normalized"] = df["Signatures_num"] / 100
    df["Servei Territorial"] = df["Servei Territorial"].fillna("Sense Servei Territorial")
    df["Comarca"] = df["Comarca"].fillna("Sense comarca")
    df["Municipi"] = df["Municipi"].fillna("Sense municipi")
    return df

st.set_page_config(layout="wide", page_title="Treemap Docents 3 nivells Drilldown")

st.title("Distribució de docents i signatures per Servei Territorial, Comarca i Municipi")

if st.button("🔄 Refresca dades"):
    st.cache_data.clear()

df = carregar_dades()

fig = px.treemap(
    df,
    path=[px.Constant("Catalunya"), "Servei Territorial", "Comarca", "Municipi"],
    values="Professorat",
    color="Signatures_normalized",
    color_continuous_scale=px.colors.sequential.Greens,
    range_color=[0, 1],
    custom_data=["Signatures(%)"],
    hover_data={
        "Servei Territorial": True,
        "Comarca": True,
        "Municipi": True,
        "Professorat": True,
        "Signatures(%)": True,
    }
)

fig.update_traces(
    texttemplate="%{label}<br>Professorat: %{value}<br>Signatures: %{customdata[0]}",
    maxdepth=1,  # 🔑 Només un nivell visible a la vegada
    branchvalues="total"
)

st.plotly_chart(fig, use_container_width=True)
