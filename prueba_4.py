import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import folium
from streamlit_folium import folium_static
import geopandas as gpd
st.set_page_config(page_title="Sismos_100") # Nombre para configurar la pagina web
st.header('Primeros 97 sismos registrados en el Peru entre 1960-2022') #Va a ser el titulo de la pagina
st.subheader('(Aun faltan más datos, solo es un Demo)') #Subtitulo

excel_file = 'prueba_project.xlsx' #Nombre archivo a importar 

sheet_name = 'Hoja1' #la hoja de excel que voy a importar

df = pd.read_excel(excel_file, #importo el archivo excel
                   sheet_name = sheet_name, #le digo cual hoja necesito
                   usecols = 'A:H', #aqui traigo las columnas que quiero usar
                   header =1) #desde que fila debe empezar a tomarme la informacion 





conteo_magnitud = df[7.5].value_counts()


df_conteo = pd.DataFrame({'MAGNITUD': conteo_magnitud.index, 'FRECUENCIA': conteo_magnitud.values})
#Rangos:
rangos = pd.cut(df[7.5], bins=5) 
# Contar las frecuencias en los rangos
conteo_rangos = rangos.value_counts().sort_index()
# Crear un nuevo DataFrame con los rangos y su frecuencia
df_conteo_rangos = pd.DataFrame({'RANGO': [str(rango) for rango in conteo_rangos.index], 'FRECUENCIA': conteo_rangos.values})

st.dataframe(df) #de esta forma nos va a mostrar el dataframe en Streamlit
st.dataframe(df_conteo)
st.write(df_conteo)
st.dataframe(df_conteo_rangos)
st.write(df_conteo)


# Crear gráfico Plotly Express
fig = px.bar(df_conteo_rangos, x='RANGO', y='FRECUENCIA', color='RANGO', labels={'FRECUENCIA': 'Frecuencia'})
fig.update_layout(title='Frecuencia de Sismos en Rangos', xaxis_title='Rango', yaxis_title='Frecuencia')

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)


#USAR LAS CORDENADAS
st.subheader('MAPA ESTATICO') 

# Configurar el mapa centrado en la primera ubicación
mapa = folium.Map(location=[df[-16.145].iloc[0], df[-72.144].iloc[0]], zoom_start=10)

# Añadir marcadores al mapa para cada ubicación en el DataFrame
for i, row in df.iterrows():
    folium.Marker([row[-16.145], row[-72.144]], popup=f"Valor: {row[7.5]}").add_to(mapa)

# Mostrar el mapa en Streamlit
folium_static(mapa)

st.subheader('GRAFICO CON SLIDER')

#GRAFICO CON SLIDER
# Crear rangos con la misma longitud para la columna '7.5'

rangos = pd.cut(df[7.5], bins=5) 
# Convertir los Intervalos a cadenas
df['Rango'] = rangos.astype(str)

# Crear sliders para seleccionar un rango de valores de '19600113'
min_value = df[19600113].min()
max_value = df[19600113].max()

min_selected_value, max_selected_value = st.slider('Selecciona un rango de valores de 19600113',
                                                    min_value, max_value, (min_value, max_value))

# Filtrar el DataFrame por el rango seleccionado
df_filtrado = df[(df[19600113] >= min_selected_value) & (df[19600113] <= max_selected_value)]

# Actualizar la gráfica de barras con el DataFrame filtrado
conteo_edades_filtrado = df_filtrado['Rango'].value_counts().sort_index()
df_conteo_filtrado = pd.DataFrame({'MAGNITUD': conteo_edades_filtrado.index, 'FRECUENCIA': conteo_edades_filtrado.values})

# Crear la gráfica de barras actualizada
fig = px.bar(df_conteo_filtrado, x='MAGNITUD', y='FRECUENCIA', color='MAGNITUD', labels={'FRECUENCIA': 'Frecuencia'})
fig.update_layout(title=f'Frecuencia de Sismos en Rangos (Valor 19600113 entre {min_selected_value} y {max_selected_value})',
                  xaxis_title='Rango', yaxis_title='Frecuencia')

# Mostrarlo en streamlit
st.plotly_chart(fig)

st.subheader('Mapa con Slider') 


#MAPA CON SLIDER:
# Crear sliders para seleccionar un rango de valores de '19600113' y '7.5'
min_value_19600113 = df[19600113].min()
max_value_19600113 = df[19600113].max()

min_selected_value_19600113, max_selected_value_19600113 = st.slider(
    'Selecciona un rango de valores de 19600113',
    min_value_19600113, max_value_19600113, (min_value_19600113, max_value_19600113),
    key="slider_19600113"  # Agrega una clave única
)

min_value_7_5 = df[7.5].min()
max_value_7_5 = df[7.5].max()

min_selected_value_7_5, max_selected_value_7_5 = st.slider(
    'Selecciona un rango de valores de 7.5',
    min_value_7_5, max_value_7_5, (min_value_7_5, max_value_7_5),
    key="slider_7_5"  # Agrega una clave única
)

# Filtrar el DataFrame por los rangos seleccionados
df_filtrado = df[
    (df[19600113] >= min_selected_value_19600113) & (df[19600113] <= max_selected_value_19600113) &
    (df[7.5] >= min_selected_value_7_5) & (df[7.5] <= max_selected_value_7_5)
]

# Actualizar el mapa con los filtros
mapa_filtrado = folium.Map(location=[df_filtrado[-16.145].iloc[0], df_filtrado[-72.144].iloc[0]], zoom_start=10)

for i, row in df_filtrado.iterrows():
    folium.Marker([row[-16.145], row[-72.144]], popup=f"Valor: {row[7.5]}").add_to(mapa_filtrado)

# Mostrar el mapa filtrado en Streamlit
folium_static(mapa_filtrado)
