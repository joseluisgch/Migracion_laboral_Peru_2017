import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

# Función para generar un diagrama de Sankey por macrozona
def generar_diagrama_sankey(data, macrozona, titulo):
    # Filtrar datos para la macrozona actual
    data_filtrada = data[data['macrozona_origen'] == macrozona]

    # Identificar los departamentos de destino relevantes
    top_destinations = (
        data_filtrada.groupby('depart_destino')['pob_c']
        .sum()
        .nlargest(10)
        .index.tolist()
    )

    # Filtrar los datos para los destinos principales
    data_filtrada = data_filtrada[data_filtrada['depart_destino'].isin(top_destinations)]

    # Crear nodos únicos para la macrozona de origen y los departamentos de destino
    origen_nodos = [f"{macrozona} (Origen)"]
    destino_nodos = [f"{dep} (Destino)" for dep in top_destinations]
    nodos = origen_nodos + destino_nodos
    nodos_dict = {nodo: i for i, nodo in enumerate(nodos)}

    # Mapear flujos a nodos
    data_filtrada['source'] = nodos_dict[f"{macrozona} (Origen)"]
    data_filtrada['target'] = data_filtrada['depart_destino'].apply(lambda x: nodos_dict[f"{x} (Destino)"])

    # Asignar colores únicos a los flujos
    color = f"rgba({random.randint(50, 255)}, {random.randint(50, 255)}, {random.randint(50, 255)}, 0.7)"
    data_filtrada['color'] = color

    # Preparar los datos para el diagrama de Sankey
    sources = data_filtrada['source'].tolist()
    targets = data_filtrada['target'].tolist()
    values = data_filtrada['pob_c'].tolist()
    colors = data_filtrada['color'].tolist()

    # Crear el gráfico Sankey
    fig = go.Figure(data=[
        go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.1),
                label=nodos,
                color="rgba(169, 169, 169, 0.7)",  # Color gris con transparencia
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=colors,
            ),
        )
    ])

    # Personalizar el diseño
    fig.update_layout(
        title_text=titulo,
        font_size=12,
        width=900,
        height=600,
    )
    return fig

def main():
    st.title("Análisis de migración laboral en Perú - 2017")
    st.write("En base a los datos del Censo de Población y Vivienda del año 2017 (INEI), se han identificado patrones de desplazamiento de la población económicamente activa ocupada (PEAO) entre las cuatro macrozonas del Perú y los 25 departamentos del país.")

    # Ruta al archivo CSV
    file_path = "C:/Users/ANALISIS SIG/2_Aplicaciones_streamlit/Dataset/Destino_trabajo_cpv17.csv"

    # Cargar los datos desde el archivo
    data = pd.read_csv(file_path, sep=";")
    data['depart_destino'] = data['depart_destino'].str.strip()
    data['macrozona_origen'] = data['macrozona_origen'].str.strip()

    # Macrozona Lima y Callao
    st.subheader("Macrozona Lima y Callao:")
    st.markdown("""  
    - Es la principal fuente de trabajadores a nivel nacional, enviando 2,434,325 personas.
    - Representa un alto porcentaje de la migración laboral entre las macrozonas.
    - Contribuye significativamente al desarrollo económico en regiones específicas.
    - Se observa una mayor concentración hacia Lima y Callao.
    """)
    fig_lima = generar_diagrama_sankey(data, "Lima - Callao", "Diagrama de Sankey: Lima y Callao")
    st.plotly_chart(fig_lima)

    # Macrozona Centro
    st.subheader("Macrozona Centro:")
    st.markdown("""  
    - Representa un flujo de 274,614 personas empleadas.
    - Tiene una alta contribución hacia Junín (98,230) y Huancavelica (37,795), lo que subraya una dinámica interna significativa dentro de la región central.
    - Otros destinos destacados son Pasco (14,115) y Lima-Callao (5,979). La relación con Lima se explica por la centralidad económica de la capital.
    """)
    fig_centro = generar_diagrama_sankey(data, "Macrozona Centro", "Diagrama de Sankey: Macrozona Centro")
    st.plotly_chart(fig_centro)

    # Macrozona Norte
    st.subheader("Macrozona Norte:")
    st.markdown("""  
    - Genera 548,265 trabajadores, siendo un aporte importante hacia regiones del norte como: 
        * La Libertad (156,141)
        * Lambayeque (97,074)
        * Piura (119,771)
    - Aunque el flujo hacia Lima-Callao es menor en comparación con otras macrozonas (21,496), sigue siendo significativo dada la atracción laboral de la capital.
    """)
    fig_norte = generar_diagrama_sankey(data, "Macrozona Norte", "Diagrama de Sankey: Macrozona Norte")
    st.plotly_chart(fig_norte)

    # Macrozona Sur
    st.subheader("Macrozona Sur:")
    st.markdown("""  
    - Con 732,470 trabajadores, muestra una importante contribución regional e interregional.
    - Los principales destinos son:
        * Arequipa (272,469): Este departamento absorbe el mayor flujo, mostrando su relevancia económica en la región sur.
        * Cusco (125,987) y Puno (57,312): Reflejan la interacción dentro de la región sur.
    - Aunque menos destacado, también hay un flujo hacia Lima-Callao (26,048), lo que evidencia la conexión con la capital.
    """)
    fig_sur = generar_diagrama_sankey(data, "Macrozona Sur", "Diagrama de Sankey: Macrozona Sur")
    st.plotly_chart(fig_sur)

if __name__ == '__main__':
    main()
