
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt  # <- Importación para histogramas
import seaborn as sns  # <- Importación necesaria para el mapa de calor
from io import BytesIO

# ---------------------
# 🎯 CONFIGURACIÓN DE LA APP
# ---------------------
st.set_page_config(page_title="Visualización de Datos", layout="wide")

st.title("📊 Aplicación de Visualización de Datos")
st.markdown("Carga un dataset, explora sus estadísticas y visualiza los datos de forma interactiva.")

# ---------------------
# 📤 CARGA DE DATOS
# ---------------------
st.sidebar.header("📥 Cargar Dataset")

uploaded_file = st.sidebar.file_uploader("Sube un archivo CSV o Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)

    st.sidebar.success("✅ Archivo cargado correctamente")

    # ---------------------
    # 🔍 ANÁLISIS EXPLORATORIO
    # ---------------------
    st.sidebar.header("🔎 Exploración")
    if st.sidebar.checkbox("Mostrar datos"):
        st.write(df)

    if st.sidebar.checkbox("Mostrar estadísticas descriptivas"):
        st.write(df.describe())

    # Filtros dinámicos
    st.sidebar.header("🔧 Filtros dinámicos")
    filter_column = st.sidebar.selectbox("Selecciona una columna para filtrar", df.columns)

    if df[filter_column].dtype == "object":
        selected_value = st.sidebar.selectbox("Selecciona un valor", df[filter_column].unique())
        filtered_df = df[df[filter_column] == selected_value]
    else:
        min_val, max_val = float(df[filter_column].min()), float(df[filter_column].max())
        range_values = st.sidebar.slider("Selecciona el rango", min_val, max_val, (min_val, max_val))
        filtered_df = df[(df[filter_column] >= range_values[0]) & (df[filter_column] <= range_values[1])]

    st.write("📊 Datos filtrados:")
    st.write(filtered_df)

    # ---------------------
    # 📊 VISUALIZACIÓN
    # ---------------------
    st.header("📈 Gráficos Interactivos")

    # Selección de columnas para gráficos
    x_col = st.selectbox("Selecciona la columna X", df.columns)
    y_col = st.selectbox("Selecciona la columna Y", df.columns)

    # Gráfico de dispersión
    fig_scatter = px.scatter(df, x=x_col, y=y_col, color=df.columns[0], title="Gráfico de Dispersión")
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Gráfico de barras
    fig_bar = px.bar(df, x=x_col, y=y_col, title="Gráfico de Barras", color=df.columns[0])
    st.plotly_chart(fig_bar, use_container_width=True)

    # Gráfico de líneas
    fig_line = px.line(df, x=x_col, y=y_col, title="Gráfico de Líneas", markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

    # ---------------------
    # 📊 HISTOGRAMAS
    # ---------------------
    st.header("📊 Histogramas")

    if st.sidebar.checkbox("Mostrar histogramas de variables numéricas"):
        fig, ax = plt.subplots(figsize=(12, 8))
        df.hist(ax=ax, bins=20)
        plt.suptitle("Distribución de Variables Numéricas")
        st.pyplot(fig)

    # ---------------------
    # 🔥 MAPA DE CALOR
    # ---------------------
    st.header("🔥 Mapa de Calor - Correlación")

    if st.sidebar.checkbox("Mostrar mapa de calor"):
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        plt.title("Mapa de Calor - Correlación")
        st.pyplot(fig)

    # ---------------------
    # 📤 EXPORTAR RESULTADOS
    # ---------------------
    st.header("📤 Exportar Datos")

    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(filtered_df)

    st.download_button(
        label="📥 Descargar datos filtrados",
        data=csv,
        file_name="datos_filtrados.csv",
        mime="text/csv",
    )

else:
    st.warning("⚠️ Carga un archivo CSV o Excel para comenzar.")

