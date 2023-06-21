import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Función para obtener el link de descarga
def create_download_link(file_id):
    return f'https://drive.google.com/uc?id={file_id}'

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

# Crear tabla de contingencia
ct = pd.crosstab(df[x_var], df[y_var])

# Mostrar la tabla
st.dataframe(ct)

# Función para mostrar el gráfico
def show_graph(ct):
    ct.plot(kind='bar', stacked=True)
    plt.title(f"Gráfico de barras de {x_var} vs {y_var}")
    plt.xlabel(x_var)
    plt.ylabel('conteo')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

# Asegurarse de que hay datos antes de intentar graficar
if not ct.empty:
    buf = show_graph(ct)
    st.download_button(
        label="Descargar gráfica",
        data=buf,
        file_name='grafica.png',
        mime='image/png'
    )
else:
    st.write("No hay datos suficientes para graficar")





