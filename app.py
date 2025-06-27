import streamlit as st
import pandas as pd
import plotly.express as px

# Llegim les dades des del Google Sheets publicat com a CSV
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSHGPTp7clJ4bIpnlqMJBwaYIHKcini9KHMrqzWGs_svIJh-jQkPGh6WlDn7_IRWVYg38nsDGBfqbxs/pub?output=csv"

@st.cache_data
def carregar_dades():
    df = pd.read_csv(URL)
    return df

df = carregar_dades()

# Assegurem que les columnes tinguin noms clars
df.columns = ["Servei Territorial", "Professorat", "Signatures (%)"]

# Color segons percentatge: 0% blanc, 100% verd intens
colors = px.colors.sequential.Greens
df["Signatures (%)"] = df["Signatures (%)"].str.replace('%', '').astype(float)
df["color"] = px.colors.sample_colorscale(colors, df["Signatures (%)"]/100)

fig = px.treemap(
    df,
    path=["Servei Territorial"],
    values="Professorat",
    color="Signatures (%)",
    color_continuous_scale="Greens",
)

fig.update_traces(textinfo="label+text+value", textfont_size=14)

st.title("Distribució dels docents per serveis territorials i signatures recollides")

st.plotly_chart(fig, use_container_width=True)

# Llegenda visual separada
st.markdown("### Llegenda de color segons % de signatures")
st.image("https://raw.githubusercontent.com/plotly/plotly.py/master/doc/img/continuous_color_scales/greens.png")
