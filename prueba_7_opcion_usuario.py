import pandas as pd
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="Sismos_100")  # Nombre para configurar la página web
st.header('Primeros 97 sismos registrados en el Perú entre 1960-2022')  # Título de la página
st.subheader('(Aún faltan más datos, solo es un Demo)')  # Subtítulo

excel_file = 'prueba_project_1000.xlsx'  # Nombre del archivo a importar
sheet_name = 'Hoja1'  # Nombre de la hoja de Excel que voy a importar

df = pd.read_excel(excel_file, sheet_name=sheet_name, usecols='A:H', header=1)

# Cambiar los nombres de las columnas
df = df.rename(columns={7.5: 'Magnitud', 19600113: 'Fecha_UTC', -16.145: 'Latitud', -72.144: 'Longitud'})

# Extraer Año, Mes y Día de la columna Fecha_UTC
df['Año'] = df['Fecha_UTC'].astype(str).str[:4]
df['Mes'] = df['Fecha_UTC'].astype(str).str[4:6]
df['Día'] = df['Fecha_UTC'].astype(str).str[6:]

conteo_magnitud = df['Magnitud'].value_counts()
df_conteo = pd.DataFrame({'MAGNITUD': conteo_magnitud.index, 'FRECUENCIA': conteo_magnitud.values})

# Rangos
rangos = pd.cut(df['Magnitud'], bins=5)
df['Rango'] = rangos.astype(str)

# DataFrame de frecuencia por rango
conteo_rangos = rangos.value_counts().sort_index()
df_conteo_rangos = pd.DataFrame({'RANGO': [str(rango) for rango in conteo_rangos.index], 'FRECUENCIA': conteo_rangos.values})

st.dataframe(df)  # Mostrar el DataFrame en Streamlit
st.dataframe(df_conteo)
st.write(df_conteo)
st.dataframe(df_conteo_rangos)
st.write(df_conteo)

# Crear gráfico Plotly Express
fig = px.bar(df_conteo_rangos, x='RANGO', y='FRECUENCIA', color='RANGO', labels={'FRECUENCIA': 'Frecuencia'})
fig.update_layout(title='Frecuencia de Sismos en Rangos', xaxis_title='Rango', yaxis_title='Frecuencia')

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

# USAR LAS CORDENADAS
st.subheader('MAPA ESTATICO')

# Configurar el mapa centrado en la primera ubicación
mapa = folium.Map(location=[df['Latitud'].iloc[0], df['Longitud'].iloc[0]], zoom_start=10)

# Añadir marcadores al mapa para cada ubicación en el DataFrame
for i, row in df.iterrows():
    folium.Marker([row['Latitud'], row['Longitud']], popup=f"Valor: {row['Magnitud']}").add_to(mapa)

# Mostrar el mapa en Streamlit
folium_static(mapa)

st.subheader('GRAFICO CON SLIDER')

# GRAFICO CON SLIDER
# Crear rangos con la misma longitud para la columna 'Magnitud'
rangos = pd.cut(df['Magnitud'], bins=5)
# Convertir los Intervalos a cadenas
df['Rango'] = rangos.astype(str)

# Crear slider para seleccionar un rango de años de 'Fecha_UTC'
min_year = df['Año'].astype(int).min()
max_year = df['Año'].astype(int).max()

selected_years = st.select_slider('Selecciona un rango de años de Fecha_UTC',
                                  options=list(range(min_year, max_year + 1)),
                                  value=(min_year, max_year),
                                  key="select_slider_19600113")

# Filtrar el DataFrame por el rango seleccionado de años
df_filtrado = df[(df['Año'].astype(int) >= selected_years[0]) & (df['Año'].astype(int) <= selected_years[1])]

# Actualizar la gráfica de barras con el DataFrame filtrado
conteo_edades_filtrado = df_filtrado['Rango'].value_counts().sort_index()
df_conteo_filtrado = pd.DataFrame({'MAGNITUD': conteo_edades_filtrado.index, 'FRECUENCIA': conteo_edades_filtrado.values})

# Crear la gráfica de barras actualizada
fig = px.bar(df_conteo_filtrado, x='MAGNITUD', y='FRECUENCIA', color='MAGNITUD', labels={'FRECUENCIA': 'Frecuencia'})
fig.update_layout(title=f'Frecuencia de Sismos en Rangos (Valor 19600113 entre {selected_years[0]} y {selected_years[1]})',
                  xaxis_title='Rango', yaxis_title='Frecuencia')

# Mostrarlo en streamlit
st.plotly_chart(fig)

st.subheader('Mapa con Opción de Selección')
# Mapa dinámico___
# Crear slider para los sismos
min_value_7_5 = df['Magnitud'].min()
max_value_7_5 = df['Magnitud'].max()

min_selected_value_7_5, max_selected_value_7_5 = st.slider(
    'Selecciona un rango de valores de Magnitud',
    min_value_7_5, max_value_7_5, (min_value_7_5, max_value_7_5),
    key="slider_7_5"
)

# MAPA CON OPCIÓN DE SELECCIÓN
# Crear opciones de selección para año y mes mínimo
min_year_option = st.selectbox('Selecciona el año mínimo', options=list(range(min_year, max_year + 1)))

min_month_option = st.selectbox('Selecciona el mes mínimo', options=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])

# Crear opciones de selección para año y mes máximo
max_year_option = st.selectbox('Selecciona el año máximo', options=list(range(min_year, max_year + 1)))

max_month_option = st.selectbox('Selecciona el mes máximo', options=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])

# Mapear los nombres de los meses a números
meses_a_numeros = {'Enero': '01', 'Febrero': '02', 'Marzo': '03', 'Abril': '04', 'Mayo': '05', 'Junio': '06', 'Julio': '07', 'Agosto': '08', 'Septiembre': '09', 'Octubre': '10', 'Noviembre': '11', 'Diciembre': '12'}

# Obtener los números de los meses
min_month_option_num = meses_a_numeros[min_month_option]
max_month_option_num = meses_a_numeros[max_month_option]

# Filtrar el DataFrame por los rangos seleccionados
df_filtrado_opcion = df[
    (df['Año'].astype(int) >= min_year_option) & (df['Mes'].astype(int) >= int(min_month_option_num)) &
    (df['Año'].astype(int) <= max_year_option) & (df['Mes'].astype(int) <= int(max_month_option_num)) &
    (df['Magnitud'] >= min_selected_value_7_5) & (df['Magnitud'] <= max_selected_value_7_5)
]

# Actualizar el mapa con los filtros de opción de selección
if not df_filtrado_opcion.empty:
    mapa_filtrado_opcion = folium.Map(location=[df_filtrado_opcion['Latitud'].iloc[0], df_filtrado_opcion['Longitud'].iloc[0]],
                                      zoom_start=10)

    for i, row in df_filtrado_opcion.iterrows():
        folium.Marker([row['Latitud'], row['Longitud']], popup=f"Valor: {row['Magnitud']}").add_to(mapa_filtrado_opcion)

    # Mostrar el mapa filtrado en Streamlit
    folium_static(mapa_filtrado_opcion)
else:
    st.warning("No hay datos disponibles para los filtros seleccionados.")
