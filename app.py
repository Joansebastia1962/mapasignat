import streamlit as st
import pandas as pd
import plotly.express as px

URL_GENERAL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSHGPTp7clJ4bIpnlqMJBwaYIHKcini9KHMrqzWGs_svIJh-jQkPGh6WlDn7_IRWVYg38nsDGBfqbxs/pub?output=csv"
URL_BARCELONES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSHGPTp7clJ4bIpnlqMJBwaYIHKcini9KHMrqzWGs_svIJh-jQkPGh6WlDn7_IRWVYg38nsDGBfqbxs/pub?gid=2070387911&single=true&output=csv"

@st.cache_data
def carregar_dades(url):
    df = pd.read_csv(url)
    df["Signatures_num"] = df["Signatures(%)"].astype(str).str.replace('%', '').astype(float)
    df["Signatures_normalized"] = df["Signatures_num"] / 100
    return df

st.set_page_config(layout="wide", page_title="Treemap Docents")

st.title("Distribució de docents i signatures")

if st.button("🔄 Refresca dades"):
    st.cache_data.clear()

opcio = st.selectbox(
    "Selecciona la visualització:",
    ["General", "Detall Barcelonès"]
)

if opcio == "General":
    df = carregar_dades(URL_GENERAL)
    st.write("Columnes General:", df.columns.tolist())
    df["Etiqueta"] = df["Signatures(%)"]
    fig = px.treemap(
        df,
        path=[px.Constant("Catalunya"), "Servei Territorial"],
        values="Professorat",
        color="Signatures_normalized",
        color_continuous_scale=px.colors.sequential.Greens,
        range_color=[0, 1],
        hover_data={
            "Servei Territorial": True,
            "Professorat": True,
            "Signatures(%)": True,
        }
    )
    fig.update_traces(textinfo="label+text", text=df["Etiqueta"])
    st.plotly_chart(fig, use_container_width=True)

elif opcio == "Detall Barcelonès":
    df = carregar_dades(URL_BARCELONES)
    st.write("Columnes Detall Barcelonès:", df.columns.tolist())
    df["Etiqueta"] = df["municipi"] + " " + df["Signatures(%)"]
    fig = px.treemap(
        df,
        path=[px.Constant("Barcelonès"), "municipi"],  # Correcte: 2 nivells!
        values="Professorat",
        color="Signatures_normalized",
        color_continuous_scale=px.colors.sequential.Greens,
        range_color=[0, 1],
        hover_data={
            "municipi": True,
            "Professorat": True,
            "Signatures(%)": True,
        }
    )
    fig.update_traces(textinfo="text", text=df["Etiqueta"])
    st.plotly_chart(fig, use_container_width=True)
