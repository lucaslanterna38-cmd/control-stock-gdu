import streamlit as st
import pandas as pd

st.set_page_config(page_title="Control de Stock", layout="centered")

@st.cache_data
def cargar_datos(archivo):
    return pd.read_excel(archivo, sheet_name=None)

file_sin_venta = "Articulos sin venta en 30 dias con Stock GDU_2.xlsx"
file_con_venta = "Articulos con venta en 30 dias sin Stock GDU.xlsx"

try:
    dict_sin_venta = cargar_datos(file_sin_venta)
    dict_con_venta = cargar_datos(file_con_venta)
    
    # Extraer nombres de sucursales excluyendo hojas de resumen
    sucursales = [s for s in dict_sin_venta.keys() if s != "GENERICO"]
    
    st.title("📦 Control de Sucursales")
    sucursal_elegida = st.selectbox("Selecciona un local:", sucursales)
    
    st.subheader("🔴 Con Stock y SIN venta (30d)")
    st.dataframe(dict_sin_venta[sucursal_elegida].dropna(how='all'), use_container_width=True)
    
    st.subheader("🟡 SIN Stock y CON venta (30d)")
    st.dataframe(dict_con_venta[sucursal_elegida].dropna(how='all'), use_container_width=True)

except FileNotFoundError:
    st.error("Esperando actualización de archivos de stock...")