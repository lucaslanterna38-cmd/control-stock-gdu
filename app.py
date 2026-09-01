import streamlit as st
import pandas as pd

st.set_page_config(page_title="Control de Stock", layout="centered")

@st.cache_data
def cargar_datos(archivo):
    return pd.read_excel(archivo, sheet_name=None)

def formatear_tabla(df):
    # 1. Limpiamos filas y columnas 100% vacías
    df_clean = df.dropna(how='all', axis=1).dropna(how='all', axis=0).reset_index(drop=True)
    
    # 2. Escribimos "Stock Leopoldo Gross" en la fila 1, última columna (reemplazando el None)
    df_clean.iloc[1, -1] = "Stock Leopoldo Gross"
    
    # 3. Convertimos esa fila 1 en los encabezados reales de la tabla
    df_clean.columns = df_clean.iloc[1]
    
    # 4. Eliminamos la fila 0 (sucursal) y la fila 1 (vieja) para dejar solo los productos
    df_clean = df_clean.iloc[2:].reset_index(drop=True)
    df_clean.columns.name = None # Limpia el nombre del índice
    
    return df_clean

def filtrar_stock_menor_50(df):
    # Forzamos la última columna a número
    stock_lg = pd.to_numeric(df.iloc[:, -1], errors='coerce')
    
    # Detectamos las filas a borrar
    filas_borrar = stock_lg <= 50
    nombres_borrar = filas_borrar.shift(-1).fillna(False)
    
    # Retornamos el dataframe limpio
    return df[~(filas_borrar | nombres_borrar)].reset_index(drop=True)

# Nombres de tus archivos actuales en GitHub
file_sin_venta = "Plano - 01-09 - Articulos sin venta en 30 dias con Stock GDU.xlsx"
file_con_venta = "Plano - 01-09 - Articulos con venta en 30 dias sin Stock GDU - copia.xlsx"

try:
    dict_sin_venta = cargar_datos(file_sin_venta)
    dict_con_venta = cargar_datos(file_con_venta)
    
    sucursales = [s for s in dict_sin_venta.keys() if s != "GENERICO"]
    
    st.title("📦 Control de Sucursales")
    sucursal_elegida = st.selectbox("Selecciona un local:", sucursales)
    
    # TABLA 1: Se formatea pero NO se filtra por <= 50
    st.subheader("🔴 Con Stock y SIN venta (30d)")
    df_sin_crudo = dict_sin_venta[sucursal_elegida]
    df_sin_formateado = formatear_tabla(df_sin_crudo)
    st.dataframe(df_sin_formateado, use_container_width=True)
    
    # TABLA 2: Se formatea Y se filtra por <= 50
    st.subheader("🟡 SIN Stock y CON venta (30d)")
    df_con_crudo = dict_con_venta[sucursal_elegida]
    df_con_formateado = formatear_tabla(df_con_crudo)
    df_con_filtrado = filtrar_stock_menor_50(df_con_formateado)
    st.dataframe(df_con_filtrado, use_container_width=True)

except FileNotFoundError:
    st.error("Esperando actualización de archivos de stock... Revisa que los nombres en GitHub coincidan.")
except Exception as e:
    st.error(f"Ocurrió un error en la plataforma: {e}")
