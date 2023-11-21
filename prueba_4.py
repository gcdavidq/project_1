import pandas as pd
import streamlit as st
from PIL import Image
st.set_page_config(page_title="Encuesta Oficial EPS") # Nombre para configurar la pagina web
st.header('Resultados Encuestas Nacionales EPS Colombia 2022') #Va a ser el titulo de la pagina
st.subheader('Cómo perciben los ciudadanos el servicio de las EPS en Colombia?') #Subtitulo

excel_file = 'Catalogo1960_2022.xlsx' #Nombre archivo a importar  'xlsx' hace referencia a excel

sheet_name = 'Catalogo1960_2022.xlsx' #la hoja de excel que voy a importar

df = pd.read_excel(excel_file, #importo el archivo excel
                   sheet_name = sheet_name, #le digo cual hoja necesito
                   usecols = 'A:D', #aqui traigo las columnas que quiero usar
                   header =3) #desde que fila debe empezar a tomarme la informacion *Empieza a contar desde 0*

df_personas = df.groupby(['EPS'], as_index = False)['EDAD PERSONA ENCUESTADA'].count() #hago un tipo de TABLA DINAMICA para agrupar los datos de una mejor manera, lo que hago aqui es que por cada EPS, me cuente la cantidad de personas encuestadas***

df_personas2 = df_personas #la guardo en otro dataframe (NO ES NECESARIO)


# Supongamos que ya tienes el DataFrame original df

# Obtener el conteo de cada valor único en 'EDAD PERSONA ENCUESTADA'
conteo_edades = df['MAGNITUD'].value_counts()

# Crear un nuevo DataFrame con 'EDAD PERSONA ENCUESTADA' y su frecuencia
df_conteo = pd.DataFrame({'MAGNITUD': conteo_edades.index, 'FRECUENCIA': conteo_edades.values})

st.dataframe(df) #de esta forma nos va a mostrar el dataframe en Streamlit
st.write(df_conteo)
st.write(df_personas2) #este nos sirve cuando no tenemos dataframe sino object****