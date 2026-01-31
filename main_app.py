import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import geopandas as gpd
import folium as fm
from groq import Groq
from sodapy import Socrata
# Importamos los objetos geométricos más comunes de Shapely
from shapely.geometry import Point, LineString, Polygon, MultiPolygon
# Importamos PyProj para manejar proyecciones
import pyproj
from pyproj import Transformer, CRS



st.set_page_config(
    page_title="EDA - Streamlit",
    layout="wide"
)

st.title("📊 Análisis Exploratorio de Datos (EDA)")

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("www.datos.gov.co", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(www.datos.gov.co,
#                  MyAppToken,
#                  username="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("vtub-3de2", limit=500000)
# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_dff=results_df['departamento_del_hecho_dane']=='Antioquia'
results_df2=results_df[results_dff]
results_df2=pd.DataFrame(results_df2)
 # ==============================
        # VISTA GENERAL
        # ==============================
        st.subheader("🔍 Vista general del dataset")
        st.write(f"**Filas:** {results_df2.shape[0]} | **Columnas:** {results_df2.shape[1]}")
        st.dataframe(results_df2.head())

        # ==============================
        # TIPOS DE DATOS
        # ==============================
        st.subheader("🧬 Tipos de datos")
        tipos = pd.DataFrame({
            "Columna": results_df2.columns,
            "Tipo de dato": results_df2.dtypes.astype(str),
            "Valores nulos": results_df2.isnull().sum()
        })
        st.dataframe(tipos)
