import streamlit as st
import pandas as pd

st.set_page_config(page_title="Control de Stock", layout="centered")

@st.cache_data
def cargar_datos(archivo):
    return pd.read_excel(archivo, sheet_name=None)

def filtrar_stock_menor_50(df):
    # Limpiamos el dataframe de filas y columnas 100% vacías
    df_clean = df.dropna(how='all', axis=1).dropna(how='all', axis=0).reset_index(drop=True)
    
    # Tomamos la última columna (Stock Leopoldo Gross) y forzamos su formato a número
    stock_lg = pd.to_numeric(df_clean.iloc[:, -1], errors='coerce')
    
    # Condición 1: La fila de datos tiene un stock de 50 o menos
    filas_borrar = stock_lg <= 50
    
    # Condición 2: La fila de arriba (el nombre del producto) también debe borrarse
    nombres_borrar = filas_borrar.shift(-1).fillna(False)
    
    # Nos quedamos solo con las filas que NO cumplen estas condiciones de borrado
    df_filtrado = df_clean[~(filas_borrar | nombres_borrar)]
    
    return df_filtrado.reset_index(drop=True)

# ⚠️ Asegúrate de que estos nombres coincidan EXACTAMENTE con los archivos que subiste a GitHub
file_sin_venta = "Plano - 01-09 - Articulos sin venta en 30 dias con Stock GDU.xlsx"
file_con_venta = "Plano - 01-09 - Articulos con venta en 30 dias sin Stock GDU - copia.xlsx"

try:
    dict_sin_venta = cargar_datos(file_sin_venta)
    dict_con_venta = cargar_datos(file_con_venta)
    
    # Extraer nombres de sucursales excluyendo pestañas genéricas o de consolidación
    sucursales = [s for s in dict_sin_venta.keys() if s != "GENERICO"]
    
    st.title("📦 Control de Sucursales")
    sucursal_elegida = st.selectbox("Selecciona un local:", sucursales)
    
    # TABLA 1: No se filtra por <= 50
    st.subheader("🔴 Con Stock y SIN venta (30d)")
    df_sin = dict_sin_venta[sucursal_elegida].dropna(how='all', axis=1).dropna(how='all', axis=0)
    st.dataframe(df_sin, use_container_width=True)
    
    # TABLA 2: Se filtra usando la función inteligente
    st.subheader("🟡 SIN Stock y CON venta (30d)")
    df_con = dict_con_venta[sucursal_elegida]
    df_con_filtrado = filtrar_stock_menor_50(df_con)
    st.dataframe(df_con_filtrado, use_container_width=True)

except FileNotFoundError:
    st.error("Esperando actualización de archivos de stock... Revisa que los nombres en GitHub coincidan.")
except Exception as e:
    st.error(f"Ocurrió un error en la plataforma: {e}")
