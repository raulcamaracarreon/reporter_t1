import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

# Función para obtener el link de descarga
def create_download_link(file_id):
    return f'https://drive.google.com/uc?id={file_id}'

# Función para mostrar gráfico

def show_graph(df, x_var, y_var, graph_type):
    plt.figure(figsize=(10, 5))

    if graph_type == "Gráfica de barras":
        sns.barplot(data=df, x=x_var, y=y_var)
    elif graph_type == "Mapa de calor":
        # Para crear un mapa de calor, necesitamos una matriz de correlación
        corr = df.corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm')
    elif graph_type == "Gráfica de líneas":
        sns.lineplot(data=df, x=x_var, y=y_var)

    plt.title(f"{graph_type} de {y_var} vs {x_var}")
    plt.xlabel(x_var)
    plt.ylabel(y_var)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

# IDs de tus archivos en Google Drive
docentes_pre_id = '14dI5IetWsflUprLyURLYSC1XMWLLQ6BO'
docentes_pri_id = '1mbV_IqFtAdYtCzbCVQSgA4rD_VViqe4M'
docentes_sec_id = '12X7aNLjtgubaKWaKp_fmfmGplCRQAk-H'

try:
    # Cargando los datos
    directores_url = 'https://raw.githubusercontent.com/raulcamaracarreon/reporter_t1/main/SPE2022_Dir_BD.csv'
    directores = pd.read_csv(directores_url)

    docentes_pre = pd.read_csv(create_download_link(docentes_pre_id))
    docentes_pri = pd.read_csv(create_download_link(docentes_pri_id))
    docentes_sec = pd.read_csv(create_download_link(docentes_sec_id))

except Exception as e:
    st.write(f"Ha ocurrido un error al cargar los datos: {e}")

# Agregando columna de nivel educativo a cada dataframe de docentes
docentes_pre['nivel_educativo'] = 'Preescolar'
docentes_pri['nivel_educativo'] = 'Primaria'
docentes_sec['nivel_educativo'] = 'Secundaria'

# Combinar todas las bases de datos de docentes
docentes = pd.concat([docentes_pre, docentes_pri, docentes_sec])

# Opciones de roles
role_option = st.selectbox(
    "Selecciona un rol",
    ("Directores", "Docentes")
)

if role_option == "Directores":
    df = directores
else:
    # Opciones de niveles
    nivel_option = st.selectbox(
        "Selecciona un nivel",
        ("Todos", "Preescolar", "Primaria", "Secundaria")
    )
    if nivel_option != "Todos":
        df = docentes[docentes['nivel_educativo'] == nivel_option.lower()]
    else:
        df = docentes

# Verificar si el DataFrame no está vacío
if df.empty:
    st.write("No hay datos disponibles")
else:
    try:
        st.write(df.info())
        st.write(df.head())
    except Exception as e:
        st.write(f"Ha ocurrido un error al visualizar los datos: {e}")

x_var = st.selectbox("Selecciona la variable para el eje X", df.columns)
y_var = st.selectbox("Selecciona la variable para el eje Y", df.columns)

graph_type = st.selectbox(
    "Selecciona un tipo de gráfica",
    ("Gráfica de barras", "Mapa de calor", "Gráfica de líneas")
)

# Asegurarse de que hay datos antes de intentar graficar
if not df[x_var].empty and not df[y_var].empty:
    buf = show_graph(df, x_var, y_var, graph_type)
else:
    st.write("No hay datos suficientes para graficar")

st.download_button(
    label="Descargar gráfica",
    data=buf,
    file_name='grafica.png',
    mime='image/png'
)




