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
