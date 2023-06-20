import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

# Función para obtener el link de descarga
def create_download_link(file_id):
    return f'https://drive.google.com/uc?id={file_id}'

# IDs de tus archivos en Google Drive
directores_id = '18ZZ_AOXLef3cIu24rvtO3YmNM-CS9CxH'
docentes_pre_id = '14dI5IetWsflUprLyURLYSC1XMWLLQ6BO'
docentes_pri_id = '1mbV_IqFtAdYtCzbCVQSgA4rD_VViqe4M'
docentes_sec_id = '12X7aNLjtgubaKWaKp_fmfmGplCRQAk-H'

# Cargando los datos
directores = pd.read_csv(create_download_link(directores_id))
docentes_pre = pd.read_csv(create_download_link(docentes_pre_id))
docentes_pri = pd.read_csv(create_download_link(docentes_pri_id))
docentes_sec = pd.read_csv(create_download_link(docentes_sec_id))


# Agregando columna de nivel educativo a cada dataframe de docentes
docentes_pre['nivel_educativo'] = 'Preescolar'
docentes_pri['nivel_educativo'] = 'Primaria'
docentes_sec['nivel_educativo'] = 'Secundaria'

# Combinar todas las bases de datos de docentes
docentes = pd.concat([docentes_pre, docentes_pri, docentes_sec])

def to_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    return b64

def show_dataframe(df):
    st.write(df)

def show_graph(df, x_var, y_var, graph_type):
    plt.figure(figsize=(10,6))
    if graph_type == "Gráfica de barras":
        if df[x_var].dtype in ['int64', 'float64'] and df[y_var].dtype in ['int64', 'float64']:
            chart = sns.barplot(data=df, x=x_var, y=y_var)
            for p in chart.patches:
                chart.annotate(format(p.get_height(), '.2f'), 
                               (p.get_x() + p.get_width() / 2., p.get_height()), 
                               ha = 'center', va = 'center', 
                               xytext = (0, 10), 
                               textcoords = 'offset points')
        else:
            ct = pd.crosstab(df[x_var], df[y_var])
            st.write(ct)  # Muestra el dataframe
            ct.plot(kind="bar", stacked=True)
    elif graph_type == "Mapa de calor":
        ct = pd.crosstab(df[x_var], df[y_var])
        st.write(ct)  # Muestra el dataframe
        sns.heatmap(ct, annot=True, fmt="d")
    elif graph_type == "Gráfica de líneas":
        if df[x_var].dtype in ['int64', 'float64'] and df[y_var].dtype in ['int64', 'float64']:
            sns.lineplot(data=df, x=x_var, y=y_var)
        else:
            ct = pd.crosstab(df[x_var], df[y_var])
            st.write(ct)  # Muestra el dataframe
            ct.plot(kind="line")

    st.pyplot(plt.gcf())  # Agrega esta línea para mostrar la gráfica

    # Guardar la gráfica en un objeto BytesIO
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    return buf

# Opciones de roles
role_option = st.selectbox(
    "Selecciona un rol",
    ("Directores", "Docentes")
)

if role_option == "Directores":
    df = directores
    show_dataframe(df)
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

    show_dataframe(df)

x_var = st.selectbox("Selecciona la variable para el eje X", df.columns)
y_var = st.selectbox("Selecciona la variable para el eje Y", df.columns)

graph_type = st.selectbox(
    "Selecciona un tipo de gráfica",
    ("Gráfica de barras", "Mapa de calor", "Gráfica de líneas")
)

buf = show_graph(df, x_var, y_var, graph_type)



st.download_button(
    label="Descargar gráfica",
    data=buf,
    file_name='grafica.png',
    mime='image/png'
)
