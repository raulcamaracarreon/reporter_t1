import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

# Cargando los datos localmente
directores = pd.read_csv('SPE2022_Dir_BD.csv')
docentes_pre = pd.read_csv('SPE2022_Doc_Pre_BD.csv')
docentes_pri_1 = pd.read_csv('SPE2022_Doc_Pri_BD_1.csv')
docentes_pri_2 = pd.read_csv('SPE2022_Doc_Pri_BD_2.csv')

# Combinar los dos archivos de docentes de primaria
docentes_pri = pd.concat([docentes_pri_1, docentes_pri_2])

# Cargamos los archivos de docentes de secundaria
docentes_sec_1 = pd.read_csv('SPE2022_Doc_Sec_BD_1.csv')
docentes_sec_2 = pd.read_csv('SPE2022_Doc_Sec_BD_2.csv')
docentes_sec_3 = pd.read_csv('SPE2022_Doc_Sec_BD_3.csv')
docentes_sec_4 = pd.read_csv('SPE2022_Doc_Sec_BD_4.csv')
docentes_sec_5 = pd.read_csv('SPE2022_Doc_Sec_BD_5.csv')
docentes_sec_6 = pd.read_csv('SPE2022_Doc_Sec_BD_6.csv')
docentes_sec_7 = pd.read_csv('SPE2022_Doc_Sec_BD_7.csv')

# Combinar todos los archivos de docentes de secundaria
docentes_sec = pd.concat([docentes_sec_1, docentes_sec_2, docentes_sec_3, docentes_sec_4, docentes_sec_5, docentes_sec_6, docentes_sec_7])

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
    x_var = st.selectbox("Selecciona la variable para el eje X", df.columns)
    y_var = st.selectbox("Selecciona la variable para el eje Y", df.columns)

    # Crear tabla de contingencia
    ct = pd.crosstab(df[x_var], df[y_var])

    # Crear tabla de contingencia de porcentajes
    ct_pct = ct.apply(lambda r: r/r.sum()*100, axis=1)

    # Mostrar las tablas
    st.write("Tabla de Conteo")
    st.dataframe(ct)

    st.download_button(
        label="Descargar tabla de conteo",
        data=ct.to_csv(index=True).encode(),
        file_name='tabla_conteo.csv',
        mime='text/csv'
    )

    st.write("Tabla de Porcentajes")
    st.dataframe(ct_pct)

    st.download_button(
        label="Descargar tabla de porcentajes",
        data=ct_pct.to_csv(index=True).encode(),
        file_name='tabla_porcentajes.csv',
        mime='text/csv'
    )

    # Función para crear el gráfico
    def create_graph(ct_pct):
        fig, ax = plt.subplots()
        ct_pct.plot(kind='bar', stacked=True, ax=ax)
        plt.title(f"Gráfico de barras de {x_var} vs {y_var}")
        plt.xlabel(x_var)
        plt.ylabel('Porcentaje')
        return fig

    # Función para guardar el gráfico
    def save_graph(fig):
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        return buf

    # Asegurarse de que hay datos antes de intentar graficar
    if not ct_pct.empty:
        fig = create_graph(ct_pct)
        st.pyplot(fig)  # mostrar la gráfica
        buf = save_graph(fig)
        st.download_button(
            label="Descargar gráfica",
            data=buf,
            file_name='grafica.png',
            mime='image/png'
        )
    else:
        st.write("No hay datos suficientes para graficar")




