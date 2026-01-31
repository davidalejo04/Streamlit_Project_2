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

# ==============================
# ASISTENTE IA - CONFIG
# ==============================
st.sidebar.header("🤖 Asistente de análisis (IA)")

groq_api_key = st.sidebar.text_input(
    "Ingresa tu Groq API Key",
    type="password",
    help="La API Key no se guarda"
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
def ask_ai_about_data(df, user_question, api_key):
    client = Groq(api_key=api_key)

    # Resumen compacto del dataset
    data_context = f"""
    Dataset cargado:
    - Filas: {df.shape[0]}
    - Columnas: {df.shape[1]}
    - Columnas: {list(df.columns)}

    Estadísticas principales:
    {df.describe(include="all").to_string()}
    """

    prompt = f"""
    Eres un analista de datos senior.
    Analiza el dataset y responde con lenguaje claro,
    insights accionables y conclusiones útiles.

    CONTEXTO:
    {data_context}

    PREGUNTA DEL USUARIO:
    {user_question}
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Eres un experto en análisis exploratorio de datos."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=700
    )

    return completion.choices[0].message.content
    
        # ==========================
        # ASISTENTE DE ANÁLISIS IA
        # ==========================
st.subheader("🤖 Asistente inteligente de análisis")

        user_question = st.text_area(
            "Haz una pregunta sobre el dataset",
            placeholder=(
                "Ej: ¿Qué ciudades presentan mayor contaminación?\n"
                "Ej: ¿Observas anomalías en PM2.5?\n"
                "Ej: Resume los hallazgos más importantes"
            )
        )

        if st.button("🔍 Analizar con IA"):
            if not groq_api_key:
                st.warning("⚠️ Ingresa tu Groq API Key en la barra lateral")
            elif not user_question.strip():
                st.warning("⚠️ Escribe una pregunta")
            else:
                with st.spinner("Analizando los datos con IA..."):
                    try:
                        response = ask_ai_about_data(
                            df=df,
                            user_question=user_question,
                            api_key=groq_api_key
                        )
                        st.markdown("### 📌 Respuesta del asistente")
                        st.markdown(response)
                    except Exception as e:
                        st.error("❌ Error al consultar la IA")
                        st.exception(e)
