
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors

SHEET_ID = "1gGUufZyh5lZSa5NVzpz725Rwifxhc4OyYgoKju4yYeo"
SHEET_NAME = "Full1"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

st.set_page_config(layout="wide")
st.title("Distribució de docents i signatures per Servei Territorial")

@st.cache_data(ttl=600)
def carregar_dades():
    return pd.read_csv(URL)

df = carregar_dades()

# (Aquí va el codi complet del gràfic que ja tens a la versió llarga)
st.write(df)
