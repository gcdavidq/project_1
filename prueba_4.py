import streamlit as st
import folium as fl
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import pandas as pd
import plotly.express as px

##################################################

st.button("Reset", type="primary")
if st.button('Say hello'):
    st.write('Why hello there')
else:
    st.write('Goodbye')

genre = st.radio(
    "What's your favorite movie genre",
    [":rainbow[Comedy]", "***Drama***", "Documentary :movie_camera:"]
)


##################################################
############################
# ruta_de_archivo = "Catalogo1960_2022.xlsx"

# # Leer el archivo Excel
# df = pd.read_excel(ruta_de_archivo, engine="openpyxl")
# # Mostrar el DataFrame en Streamlit
# st.write(df)

############################
# Leemos nuestro data set
df = pd.read_excel("Catalogo1960_2022.xlsx")

# Extraemos Año, Mes y Día de la columna Fecha_UTC del data set
df["Anio"] = df["FECHA_UTC"].astype(str).str[:4]
df["Mes"] = df["FECHA_UTC"].astype(str).str[4:6]
df["Dia"] = df["FECHA_UTC"].astype(str).str[6:]

# Encontramos el mínimo y el máximo de años comprendidos
min_anio = df["Anio"].astype(int).min()
max_anio = df["Anio"].astype(int).max()

selected_min_anio = min_anio
selected_max_anio = max_anio

anios_comprendidos = []
for i in range(min_anio, max_anio + 1):
    anios_comprendidos.append(i)
######################################################################################


    
######################################################################################

# Título 
st.title("Análisis Sísmico Registrados en el Perú (1960-2022)")

# Subtítulo n°1


st.divider()
# Subtítulo n°2
st.header("Mapa de calor de eventos sísmicos por concurrencia en zonas geográficas\
           y distribución por profundidad")

col1, col2 = st.columns(2)
col3, colo4 = st.columns(2)
with col1:
    # Selección del tipo de búsqueda
    st.write("Seleccione la foma de búsqueda:")
    opcion = st.radio(
        "Mostrar los eventos por",
        ["**Mapa de calor**","**Distribución por porfundidad**"],
        captions = ["*con opción de búsqueda por fechas.*", "*con opción de búsqueda por fechas.*"],
        index=None)
with col2:   
    # Mostraremos la información correspondiente a la opción seleccionada
    st.markdown(f"*Filtro de información de: {opcion}*")

if opcion == None:
    # Inicializamos la previsualización con el mapa centrado 
    mapa = fl.Map(location=[-9.189967, -75.015152], zoom_start=5)
    folium_static(mapa) 
   
if opcion == "**Mapa de calor**":
    with col2:
        op_fecha1 = st.selectbox(
            "Por",
            ("años puntuales", "rango de años"),
            index=None, placeholder="Seleccione . . .")
        
        if op_fecha1 == "años puntuales":
            fe_punt = st.multiselect(
                "El año puntual de búsqueda es:",
                anios_comprendidos, placeholder="elija")
            
            if fe_punt:
                # Almacenamos los años puntuales seleccionados para después usarlos como filtro
                fe_punt = list(map(int, fe_punt))

                # Filtrarmos el DataFrame para incluir solo los años seleccionados
                df_filtrado_opcion = df[df['Anio'].astype(int).isin(fe_punt)]

                mapa = fl.Map(location=[df_filtrado_opcion['LATITUD'].mean(), df_filtrado_opcion['LONGITUD'].mean()], 
                            zoom_start=5.5, max_zoom=10, control_scale=True, width="100%", height="100%")

                for index, row in df_filtrado_opcion.iterrows():
                    fl.Marker([row['LATITUD'], row['LONGITUD']],
                                popup=f"Profundidad: {row['PROFUNDIDAD']} km\nMagnitud: {row['MAGNITUD']}").add_to(mapa)

                heat_data = [[row['LATITUD'], row['LONGITUD']] for index, row in df_filtrado_opcion.iterrows()]
                HeatMap(heat_data, name='Mapa de Calor', radius=50, max_zoom=15).add_to(mapa)
                
                with col3:
                  folium_static(mapa)
            else: 
                with col3: 
                    mapa = fl.Map(location=[-9.189967, -75.015152], zoom_start=5)
                    folium_static(mapa)
        
        elif op_fecha1 == "rango de años":
            min_anio_option = st.selectbox('Selecciona el año mínimo', options=list(range(min_anio, max_anio + 1)), 
                                           index=None, placeholder="elija")
            if min_anio_option is not None:
                if min_anio_option >= min_anio: 
                    max_anio_option = st.selectbox('Selecciona el año máximo', 
                                                   options=list(range(min_anio_option, max_anio + 1)))
                    max_anio = max_anio_option  
                    min_anio = min_anio_option 

                    df_filtrado_opcion = df[
                        (df['Anio'].astype(int) >= min_anio) & (df['Anio'].astype(int) <= max_anio)
                    ]
                mapa = fl.Map(location=[df_filtrado_opcion['LATITUD'].mean(), df_filtrado_opcion['LONGITUD'].mean()], 
                            zoom_start=5.5, max_zoom=10, control_scale=True, width="100%", height="100%")

                for index, row in df_filtrado_opcion.iterrows():
                    fl.Marker([row['LATITUD'], row['LONGITUD']],
                                popup=f"Profundidad: {row['PROFUNDIDAD']} km\nMagnitud: {row['MAGNITUD']}").add_to(mapa)

                heat_data = [[row['LATITUD'], row['LONGITUD']] for index, row in df_filtrado_opcion.iterrows()]
                HeatMap(heat_data, name='Mapa de Calor', radius=50, max_zoom=15).add_to(mapa)
                
                with col3:
                  folium_static(mapa)
            else: 
                with col3: 
                    mapa = fl.Map(location=[-9.189967, -75.015152], zoom_start=5)
                    folium_static(mapa) 
        else: 
            with col3: 
                mapa = fl.Map(location=[-9.189967, -75.015152], zoom_start=5)
                folium_static(mapa) 

if opcion == "**Distribución por porfundidad**":
    with col2:
        op_fecha2 = st.selectbox(
            "Por",
            ("años puntuales", "rango de años"),
            index=None, placeholder="Seleccione . . .")
        
        
        if op_fecha2 == "años puntuales":
            fe_punt = st.multiselect(
                "El año puntual de búsqueda es:",
                anios_comprendidos, placeholder="elija")

            if fe_punt:
                # Almacenamos los años puntuales seleccionados para después usarlos como filtro
                fe_punt = list(map(int, fe_punt))

                # Filtrarmos el DataFrame para incluir solo los años seleccionados
                df_filtrado_opcion = df[df['Anio'].astype(int).isin(fe_punt)]

                color_ub = ""                                   
                mapa = fl.Map(location=[df_filtrado_opcion['LATITUD'].mean(), df_filtrado_opcion['LONGITUD'].mean()], 
                            zoom_start=5, max_zoom=12, control_scale=True)

                for index, row in df_filtrado_opcion.iterrows():
                    if row['PROFUNDIDAD'] < 70:
                        color_ub = "red"
                    elif (row['PROFUNDIDAD'] >= 70) and (row['PROFUNDIDAD'] < 300):
                        color_ub = "orange"
                    elif row['PROFUNDIDAD'] >= 300:
                        color_ub = "green"

                    fl.Marker([row['LATITUD'], row['LONGITUD']], icon=fl.Icon(color=color_ub, icon="circle", prefix="fa"),
                            popup=f"Profundidad: {row['PROFUNDIDAD']} km\nMagnitud: {row['MAGNITUD']}").add_to(mapa)

                # Construimos la leyenda en HTML
                legend_html = """
                    <div style="position: fixed; 
                                bottom: 50px; left: 50px; width: 150px; height: 100px; 
                                border:3px solid grey; z-index:9999; font-size:14px;
                                background-color:white;text-align: center;
                                border-radius: 6px;">
                        &nbsp; <span style="text-decoration: underline;", class="font-monospace">Leyenda</span> <br>
                        &nbsp; <span class="font-monospace">Superficiales</span> &nbsp; 
                        <i class="fa fa-map-marker" style="color:red"></i><br>
                        &nbsp; <span class="font-monospace">Intermedios</span> &nbsp; 
                        <i class="fa fa-map-marker" style="color:orange"></i><br>
                        &nbsp; <span class="font-monospace">Profundos</span> &nbsp; 
                        <i class="fa fa-map-marker" style="color:green"></i><br>
                    </div>
                """
                # Convertimos la leyenda HTML a un objeto de Folium
                legend = fl.Element(legend_html)
                # Agregamos la leyenda al mapa
                mapa.get_root().html.add_child(legend)
                # Mostramos el mapa en Streamlit
                with col3:
                  st.components.v1.html(mapa._repr_html_(), width=800, height=600)
            else:
                with col3: 
                    mapa = fl.Map(location=[-9.189967, -75.015152], zoom_start=5)
                    folium_static(mapa) 


        elif op_fecha2 == "rango de años":
            min_anio_option = st.selectbox('Selecciona el año mínimo', options=list(range(min_anio, max_anio + 1)), 
                                           index=None, placeholder="elija")
            if min_anio_option is not None:
                if min_anio_option >= min_anio: 
                    max_anio_option = st.selectbox('Selecciona el año máximo', 
                                                   options=list(range(min_anio_option, max_anio + 1)))
                    max_anio = max_anio_option  
                    min_anio = min_anio_option      
                    
                    df_filtrado_opcion = df[
                        (df['Anio'].astype(int) >= min_anio) & (df['Anio'].astype(int) <= max_anio)
                    ]

                color_ub = ""                                   
                mapa = fl.Map(location=[df_filtrado_opcion['LATITUD'].mean(), df_filtrado_opcion['LONGITUD'].mean()], 
                            zoom_start=5, max_zoom=12, control_scale=True)

                for index, row in df_filtrado_opcion.iterrows():
                    if row['PROFUNDIDAD'] < 70:
                        color_ub = "red"
                    elif (row['PROFUNDIDAD'] >= 70) and (row['PROFUNDIDAD'] < 300):
                        color_ub = "orange"
                    elif row['PROFUNDIDAD'] >= 300:
                        color_ub = "green"

                    fl.Marker([row['LATITUD'], row['LONGITUD']], icon=fl.Icon(color=color_ub, icon="circle", prefix="fa"),
                            popup=f"Profundidad: {row['PROFUNDIDAD']} km\nMagnitud: {row['MAGNITUD']}").add_to(mapa)

                # Construir la leyenda en HTML
                legend_html = """
                    <div style="position: fixed; 
                                bottom: 50px; left: 50px; width: 150px; height: 100px; 
                                border:3px solid grey; z-index:9999; font-size:14px;
                                background-color:white;text-align: center;
                                border-radius: 6px;">
                        &nbsp; <span style="text-decoration: underline;", class="font-monospace">Leyenda</span> <br>
                        &nbsp; <span class="font-monospace">Superficiales</span> &nbsp; 
                        <i class="fa fa-map-marker" style="color:red"></i><br>
                        &nbsp; <span class="font-monospace">Intermedios</span> &nbsp; 
                        <i class="fa fa-map-marker" style="color:orange"></i><br>
                        &nbsp; <span class="font-monospace">Profundos</span> &nbsp; 
                        <i class="fa fa-map-marker" style="color:green"></i><br>
                    </div>
                """

                # Convertir la leyenda HTML a un objeto de Folium
                legend = fl.Element(legend_html)

                # Agregar la leyenda al mapa
                mapa.get_root().html.add_child(legend)

                with col3:
                  st.components.v1.html(mapa._repr_html_(), width=800, height=600)
            else:
                with col3: 
                    mapa = fl.Map(location=[-9.189967, -75.015152], zoom_start=5)
                    folium_static(mapa) 
        else: 
            with col3: 
                mapa = fl.Map(location=[-9.189967, -75.015152], zoom_start=5)
                folium_static(mapa) 
st.divider()
# Subtítulo n°3





excel_file = 'prueba_project.xlsx'  # Nombre del archivo a importar
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
mapa = fl.Map(location=[df['Latitud'].iloc[0], df['Longitud'].iloc[0]], zoom_start=10)

# Añadir marcadores al mapa para cada ubicación en el DataFrame
for i, row in df.iterrows():
    fl.Marker([row['Latitud'], row['Longitud']], popup=f"Valor: {row['Magnitud']}").add_to(mapa)

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
    mapa_filtrado_opcion = fl.Map(location=[df_filtrado_opcion['Latitud'].iloc[0], df_filtrado_opcion['Longitud'].iloc[0]],
                                      zoom_start=10)

    for i, row in df_filtrado_opcion.iterrows():
        fl.Marker([row['Latitud'], row['Longitud']], popup=f"Valor: {row['Magnitud']}").add_to(mapa_filtrado_opcion)

    # Mostrar el mapa filtrado en Streamlit
    folium_static(mapa_filtrado_opcion)
else:
    st.warning("No hay datos disponibles para los filtros seleccionados.")
