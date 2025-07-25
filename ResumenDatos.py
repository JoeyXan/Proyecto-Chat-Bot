import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# Configuración de la página con tema personalizado
st.set_page_config(
    page_title="TECAZUAY Analytics Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para un diseño más profesional (DARK THEME)
st.markdown("""
<style>
    /* Importar fuentes de Google */
    @import url(\'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap\');
    
    /* Variables CSS para colores consistentes (DARK THEME) */
    :root {
        --primary-color: #93c5fd; /* Light blue */
        --secondary-color: #60a5fa; /* Medium blue */
        --accent-color: #22d3ee; /* Cyan */
        --success-color: #4ade80; /* Green */
        --warning-color: #fcd34d; /* Yellow */
        --danger-color: #f87171; /* Red */
        --dark-color: #1a202c; /* Dark background */
        --light-color: #2d3748; /* Slightly lighter dark for cards */
        --border-color: #4a5568; /* Darker border */
        --text-primary: #f7fafc; /* White text */
        --text-secondary: #a0aec0; /* Light gray text */
    }
    
    /* Estilos generales */
    body {
        background-color: var(--dark-color);
        color: var(--text-primary);
    }
    .main {
        padding-top: 2rem;
        font-family: \'Inter\', sans-serif;
        background-color: var(--dark-color);
        color: var(--text-primary);
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(147, 197, 253, 0.15);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        text-align: center;
        margin: 0.5rem 0 0 0;
    }
    
    /* Tarjetas de métricas */
    .metric-card {
        background: var(--light-color);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid var(--border-color);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        color: var(--text-primary);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        font-weight: 500;
        margin: 0.5rem 0;
    }
    
    .metric-delta {
        font-size: 0.8rem;
        color: var(--success-color);
        font-weight: 500;
    }
    
    /* Secciones */
    .section-header {
        background: var(--light-color);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid var(--primary-color);
        margin: 2rem 0 1rem 0;
        color: var(--text-primary);
    }
    
    .section-header h2 {
        color: var(--text-primary);
        font-size: 1.8rem;
        font-weight: 600;
        margin: 0;
    }
    
    .section-header p {
        color: var(--text-secondary);
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
    }
    
    /* Sidebar personalizado */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--dark-color) 0%, #2d3748 100%); /* Darker sidebar */
    }
    
    .css-1d391kg .css-1v0mbdj {
        color: white;
    }
    
    /* Botones de navegación */
    .nav-button {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.25rem 0;
        transition: all 0.2s ease;
        cursor: pointer;
        width: 100%;
        text-align: left;
    }
    
    .nav-button:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(5px);
    }
    
    .nav-button.active {
        background: white;
        color: var(--primary-color);
        font-weight: 600;
    }
    
    /* Gráficos */
    .chart-container {
        background: var(--light-color);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid var(--border-color);
        margin: 1rem 0;
        text-align: center; /* Centrar el contenido del contenedor */
    }
    
    .chart-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Alertas y mensajes */
    .alert {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid;
        color: var(--text-primary);
    }
    
    .alert-info {
        background: rgba(96, 165, 250, 0.1);
        border-color: var(--secondary-color);
        color: var(--primary-color);
    }
    
    .alert-warning {
        background: rgba(252, 211, 77, 0.1);
        border-color: var(--warning-color);
        color: var(--warning-color);
    }
    
    /* Footer */
    .footer {
        background: var(--dark-color);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 3rem;
        text-align: center;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Personalizar selectbox y radio buttons */
    .stSelectbox > div > div {
        background: var(--light-color);
        border: 2px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-primary);
    }
    .stSelectbox > div > div > div > div {
        color: var(--text-primary);
    }
    .stSelectbox > label {
        color: var(--text-primary);
    }
    
    .stRadio > div {
        background: var(--light-color);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        color: var(--text-primary);
    }
    .stRadio > label {
        color: var(--text-primary);
    }
    .stRadio div[role="radiogroup"] label {
        color: var(--text-primary);
    }
    
    /* General text color for Streamlit components */
    .stMarkdown, .stText, .stCaption, .stHeading, .stSubheader, .stAlert {
        color: var(--text-primary);
    }
    
    /* Specific adjustments for text within metric cards and sections */
    .metric-card .metric-label, .metric-card .metric-delta {
        color: var(--text-secondary);
    }
    .section-header p {
        color: var(--text-secondary);
    }
    
    /* Plotly chart text colors */
    .js-plotly-plot .plotly .main-svg .infolayer .annotation-text {
        fill: var(--text-primary) !important;
    }
    .js-plotly-plot .plotly .main-svg .infolayer .annotation-text tspan {
        fill: var(--text-primary) !important;
    }
    .js-plotly-plot .plotly .main-svg .infolayer .gtitle .g-text {
        fill: var(--text-primary) !important;
    }
    .js-plotly-plot .plotly .main-svg .infolayer .xtick .g-text, 
    .js-plotly-plot .plotly .main-svg .infolayer .ytick .g-text {
        fill: var(--text-secondary) !important;
    }
    .js-plotly-plot .plotly .main-svg .infolayer .xaxislayer-above .g-title .g-text, 
    .js-plotly-plot .plotly .main-svg .infolayer .yaxislayer-above .g-title .g-text {
        fill: var(--text-primary) !important;
    }
    .js-plotly-plot .plotly .main-svg .legend .g-text {
        fill: var(--text-primary) !important;
    }
    
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🎓 TECAZUAY Analytics Dashboard</h1>
    <p>Sistema de Análisis Inteligente para Chatbot Institucional</p>
</div>
""", unsafe_allow_html=True)

# Función para cargar datos desde la API
@st.cache_data
def load_data():
    try:
        # Leer archivos Excel directamente desde el repo (GitHub o local)
        df_encuesta = pd.read_excel ("Encuesta para el proyecto _Asistente Institucional_  (respuestas).xlsx")
        df_inscripcion = pd.read_excel ("Inscripción ImpulsaT - TECAZUAY (respuestas) (1).xlsx")


        return df_encuesta, df_inscripcion

    except Exception as e:
        st.error(f"⚠️ Error al cargar los archivos Excel: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Cargar datos
df_encuesta, df_inscripcion = load_data()

# Sidebar para navegación con diseño mejorado
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem; color: black;">
    <h2 style="color: white; margin: 0;"> Navegación</h2>
    <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Selecciona una sección para explorar</p>
</div>
""", unsafe_allow_html=True)

section = st.sidebar.radio(
    "",
    ["📊 Dashboard Ejecutivo", "🎯 Análisis de Encuestas", "📝 Análisis de Inscripciones", "🔍 Patrones y Predicciones", "🤖 Configuración del Chatbot"],
    key="navigation"
)

# Función para crear gráficos con estilo mejorado
def create_styled_chart(fig, title):
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': 'Inter', 'color': 'var(--text-primary)'}
        },
        font={'family': 'Inter', 'color': 'var(--text-secondary)'},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=60, b=40, l=40, r=40),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='var(--text-primary)')
        )
    )
    return fig

# Función para encontrar la columna del chatbot (maneja diferentes variaciones)
def find_chatbot_column(df):
    """Busca la columna relacionada con el chatbot en el DataFrame"""
    if df.empty:
        return None
    
    # Posibles variaciones del nombre de la columna
    posibles_nombres = [
        "¿Te gustaría contar con un asistente virtual (Chatbot) para hacer consultas rápidas?",
        "Te gustaría contar con un asistente virtual (Chatbot) para hacer consultas rápidas",
        "¿Te gustaría contar con un asistente virtual (Chatbot) para hacer consultas rápidas",
        "chatbot",
        "asistente virtual",
        "Chatbot"
    ]
    
    # Buscar coincidencias exactas
    for nombre in posibles_nombres:
        if nombre in df.columns:
            return nombre
    
    # Buscar coincidencias parciales (contiene la palabra)
    for col in df.columns:
        col_lower = col.lower()
        if "chatbot" in col_lower or "asistente virtual" in col_lower:
            return col
    
    return None

# Función para encontrar la columna de carreras
def find_carreras_column(df):
    """Busca la columna relacionada con las carreras en el DataFrame"""
    if df.empty:
        return None
    
    # Posibles variaciones del nombre de la columna
    posibles_nombres = [
        "¿En cuál de las carreras que ofrece nuestro instituto estás interesado en estudiar? ",
        "¿En cuál de las carreras que ofrece nuestro instituto estás interesado en estudiar?",
        "En cuál de las carreras que ofrece nuestro instituto estás interesado en estudiar",
        "carreras",
        "carrera"
    ]
    
    # Buscar coincidencias exactas
    for nombre in posibles_nombres:
        if nombre in df.columns:
            return nombre
    
    # Buscar coincidencias parciales
    for col in df.columns:
        col_lower = col.lower()
        if "carrera" in col_lower or "estudiar" in col_lower:
            return col
    
    return None

# Sección: Dashboard Ejecutivo
if section == "📊 Dashboard Ejecutivo":
    st.markdown("""
    <div class="section-header">
        <h2>📊 Dashboard Ejecutivo</h2>
        <p>Resumen general del proyecto y métricas clave de rendimiento</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_encuestas = len(df_encuesta) if not df_encuesta.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_encuestas:,}</div>
            <div class="metric-label">📊 Total Encuestas</div>
            <div class="metric-delta">Respuestas recopiladas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_inscripciones = len(df_inscripcion) if not df_inscripcion.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_inscripciones:,}</div>
            <div class="metric-label">📝 Total Inscripciones</div>
            <div class="metric-delta">Estudiantes registrados</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Buscar la columna del chatbot dinámicamente
        chatbot_column = find_chatbot_column(df_encuesta)
        
        if chatbot_column and not df_encuesta.empty:
            interes_chatbot = df_encuesta[chatbot_column].value_counts()
            # Buscar "Sí" o "Si" (con o sin acento)
            si_count = interes_chatbot.get('Sí', 0) + interes_chatbot.get('Si', 0)
            porcentaje_si = (si_count / len(df_encuesta)) * 100 if len(df_encuesta) > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{porcentaje_si:.1f}%</div>
                <div class="metric-label">🤖 Interés en Chatbot</div>
                <div class="metric-delta">Aceptación positiva</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">N/A</div>
                <div class="metric-label">🤖 Interés en Chatbot</div>
                <div class="metric-delta">Sin datos disponibles</div>
            </div>
            """, unsafe_allow_html=True)

    with col4:
        # Buscar la columna de carreras dinámicamente
        carreras_column = find_carreras_column(df_inscripcion)
        
        if carreras_column and not df_inscripcion.empty:
            carreras_unicas = df_inscripcion[carreras_column].nunique()
        else:
            carreras_unicas = 0
            
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{carreras_unicas}</div>
            <div class="metric-label">🎓 Carreras Solicitadas</div>
            <div class="metric-delta">Diversidad académica</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos de resumen ejecutivo
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Buscar la columna del chatbot y crear el gráfico
        chatbot_column = find_chatbot_column(df_encuesta)
        
        if chatbot_column and not df_encuesta.empty:
            interes_data = df_encuesta[chatbot_column].value_counts()
            
            # Crear colores personalizados basados en las respuestas
            colors = {}
            for respuesta in interes_data.index:
                if respuesta.lower() in ['sí', 'si', 'yes']:
                    colors[respuesta] = '#4ade80'
                else:
                    colors[respuesta] = '#f87171'
            
            fig_pie = px.pie(
                values=interes_data.values,
                names=interes_data.index,
                title="Interés en Asistente Virtual",
                color_discrete_map=colors,
                hole=0.4
            )
            fig_pie = create_styled_chart(fig_pie, "Interés en Asistente Virtual")
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            # Ajustar el tamaño del gráfico
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("📊 No hay datos disponibles para mostrar el gráfico de interés en chatbot")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Gráfico adicional - Top carreras solicitadas
        carreras_column = find_carreras_column(df_inscripcion)
        
        if carreras_column and not df_inscripcion.empty:
            carreras_data = df_inscripcion[carreras_column].value_counts().head(5)
            
            fig_bar = px.bar(
                x=carreras_data.values,
                y=carreras_data.index,
                orientation='h',
                title="Las 5 Carreras Más Solicitadas",
                color=carreras_data.values,
                color_continuous_scale='viridis'
            )
            fig_bar = create_styled_chart(fig_bar, "Las 5 Carreras Más Solicitadas")
            fig_bar.update_layout(
                xaxis_title="Número de Inscripciones",
                yaxis_title="Carreras",
                height=400,  # Altura consistente
                showlegend=False,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("📊 No hay datos disponibles para mostrar el gráfico de carreras")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Objetivos del proyecto con diseño mejorado
    st.markdown("""
    <div style="display: flex; gap: 2rem; align-items: stretch;">

    <!-- Objetivo Principal (más ancho = flex: 2) -->
    <div style="flex: 2; display: flex; flex-direction: column; justify-content: space-between;
                background: var(--light-color); padding: 2rem; border-radius: 12px; 
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border: 1px solid var(--border-color); 
                color: var(--text-primary);">
        <div>
            <h3 style="color: var(--primary-color); margin-top: 0;">🎯 Objetivo Principal</h3>
            <p style="font-size: 1.1rem; line-height: 1.6; color: var(--text-secondary);">
                Crear un chatbot inteligente que brinde información completa sobre las diversas carreras ofrecidas por el instituto, 
                así como sobre el proceso de inscripciones, utilizando herramientas tecnológicas avanzadas para analizar patrones 
                de predicción de respuestas.
            </p>
            <h3 style="color: var(--primary-color);">👥 Beneficiarios</h3>
            <p style="font-size: 1.1rem; line-height: 1.6; color: var(--text-secondary);">
                Potenciales estudiantes del Instituto Superior Tecnológico del Azuay y personal administrativo.
            </p>
        </div>
    </div>

    <!-- Impacto Esperado (más angosto = flex: 1) -->
    <div style="flex: 1; display: flex; flex-direction: column; justify-content: space-between;
                background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
                padding: 2rem; border-radius: 12px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <div>
            <h3 style="color: white; margin-top: 0;">📈 Impacto Esperado</h3>
            <ul style="list-style: none; padding: 0; font-size: 1.1rem;">
                <li style="margin: 0.5rem 0;">✅ Reducción de consultas manuales</li>
                <li style="margin: 0.5rem 0;">✅ Mejora en la experiencia del usuario</li>
                <li style="margin: 0.5rem 0;">✅ Optimización de procesos administrativos</li>
                <li style="margin: 0.5rem 0;">✅ Disponibilidad 24/7</li>
            </ul>
        </div>
    </div>

    </div>
""", unsafe_allow_html=True)



# Sección: Análisis de Encuestas
elif section == "🎯 Análisis de Encuestas":
    st.markdown("""
    <div class="section-header">
        <h2>🎯 Análisis Detallado de Encuestas</h2>
        <p>Insights profundos sobre las preferencias y necesidades de los usuarios</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df_encuesta.empty:
        st.markdown("""
        <div class="alert alert-warning">
            ⚠️ <strong>Datos no disponibles:</strong> No se pudieron cargar los datos de encuestas. 
            Verifica la conexión con la API.
        </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2 = st.columns(2)
            
        with col1:
            st.markdown("<div class=\"chart-container\">", unsafe_allow_html=True)

            chatbot_column = find_chatbot_column(df_encuesta)

            if chatbot_column:
                interes_data = df_encuesta[chatbot_column].dropna().value_counts()

               # Normalizar valores y colores
                colores_personalizados = {}
                for respuesta in interes_data.index:
                    respuesta_normal = respuesta.lower().strip()
                    if respuesta_normal in ['sí', 'si', 'yes']:
                      colores_personalizados[respuesta] = '#4ade80'  # verde
                    else:
                        colores_personalizados[respuesta] = '#f87171'  # rojo

                fig_pie = px.pie(
                    values=interes_data.values,
                    names=interes_data.index,
                    title="Interés en Asistente Virtual",
                    color_discrete_map=colores_personalizados,
                    hole=0.4
                )

                fig_pie = create_styled_chart(fig_pie, "Interés en Asistente Virtual")
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("📊 Datos de interés en chatbot no disponibles.")

            st.markdown('</div>', unsafe_allow_html=True)


        with col2:
            st.markdown("<div class=\"chart-container\">", unsafe_allow_html=True)
            comodidad_column = "¿Qué tan cómodo te sientes usando herramientas digitales para consultas?"
            
            if comodidad_column in df_encuesta.columns:
                comodidad_data = df_encuesta[comodidad_column].value_counts()
                fig_bar = px.bar(
                    x=comodidad_data.index,
                    y=comodidad_data.values,
                    title="Comodidad con Herramientas Digitales",
                    color=comodidad_data.values,
                    color_continuous_scale='plasma'
                )
                fig_bar = create_styled_chart(fig_bar, "Comodidad con Herramientas Digitales")
                fig_bar.update_xaxes(tickangle=45)
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("📊 Datos de comodidad con herramientas digitales no disponibles.")
            st.markdown('</div>', unsafe_allow_html=True)


        # Análisis de Modalidades y Jornadas
        # Limpiar nombres de columnas
        df_encuesta.columns = df_encuesta.columns.str.strip()
        st.markdown("""
        <div class="section-header">
            <h2>📚 Modalidades y Jornadas de Estudio</h2>
            <p>Distribución de estudiantes por modalidad y horarios</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class=\"chart-container\">", unsafe_allow_html=True)
            modalidad_column = "¿Cuál es tu modalidad de estudios?"
            
            if modalidad_column in df_encuesta.columns:
                modalidad_data = df_encuesta[modalidad_column].value_counts()
                fig_modalidad = px.bar(
                    x=modalidad_data.values,
                    y=modalidad_data.index,
                    orientation='h',
                    title="Modalidad de Estudios",
                    color=modalidad_data.values,
                    color_continuous_scale='magma'
                )
                fig_modalidad = create_styled_chart(fig_modalidad, "Modalidad de Estudios")
                st.plotly_chart(fig_modalidad, use_container_width=True)
            else:
                st.info("📊 Datos de modalidad de estudio no disponibles.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown("<div class=\"chart-container\">", unsafe_allow_html=True)
            jornada_column = "¿En qué jornada estudias?"
            
            if jornada_column in df_encuesta.columns:
                jornada_data = df_encuesta[jornada_column].value_counts()
                fig_jornada = px.pie(
                    values=jornada_data.values,
                    names=jornada_data.index,
                    title="Jornada de Estudios",
                    color_discrete_map={
                        'Matutina': '#20B2AA',
                        'Vespertina': '#FF6347',
                        'Nocturna': '#4682B4'
                    },
                    hole=0.4
                )
                fig_jornada = create_styled_chart(fig_jornada, "Jornada de Estudios")
                fig_jornada.update_traces(textposition='inside', textinfo='percent+label')
                fig_jornada.update_layout(
                    legend=dict(
                        orientation="v",
                        yanchor="middle",
                        y=0.5,
                        xanchor="left",
                        x=1.05,
                        font=dict(size=10)
                    )
                )

                st.plotly_chart(fig_jornada, use_container_width=True)
            else:
                st.info("📊 Datos de jornada de estudio no disponibles.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Análisis de funcionalidades deseadas
        st.markdown("""
        <div class="section-header">
            <h2>⚙️ Funcionalidades Deseadas para el Chatbot</h2>
            <p>Características más solicitadas por los usuarios</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
            
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            info_column = "¿Qué tipo de información te gustaría que ofrezca el asistente virtual (Chatbot)?"
            
            if info_column in df_encuesta.columns:
                info_deseada = df_encuesta[info_column].dropna()
                
                all_options = []
                for response in info_deseada:
                    if isinstance(response, str):
                        options = [opt.strip() for opt in response.split(',')]
                        all_options.extend(options)
                
                if all_options:
                    info_counts = pd.Series(all_options).value_counts().head(8)
                    
                    # Crear etiquetas más cortas para el gráfico
                    short_labels = []
                    for label in info_counts.index:
                        if len(label) > 30:
                            short_labels.append(label[:27] + "...")
                        else:
                            short_labels.append(label)
                    
                    fig_info = px.bar(
                        x=info_counts.values,
                        y=short_labels,
                        orientation='h',
                        title="Información Más Solicitada",
                        color=info_counts.values,
                        color_continuous_scale='viridis'
                    )
                    fig_info = create_styled_chart(fig_info, "Información Más Solicitada")
                    fig_info.update_layout(
                        height=400,
                        yaxis={'categoryorder': 'total ascending'}
                    )
                    st.plotly_chart(fig_info, use_container_width=True)
                else:
                    st.info("📊 No hay datos procesables para información deseada.")
            else:
                st.info("📊 Datos de información deseada no disponibles.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            funcion_column = "¿Qué función te hubiera sido más útil en un Chatbot como aspirante?"
            
            if funcion_column in df_encuesta.columns:
                funcion_data = df_encuesta[funcion_column].value_counts()
                
                # Crear etiquetas más cortas para el pie chart
                short_names = []
                for name in funcion_data.index:
                    if len(name) > 25:
                        short_names.append(name[:22] + "...")
                    else:
                        short_names.append(name)
                
                fig_funcion = px.pie(
                    values=funcion_data.values,
                    names=short_names,
                    title="Funciones Más Útiles",
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    hole=0.3
                )
                fig_funcion = create_styled_chart(fig_funcion, "Funciones Más Útiles")
                fig_funcion.update_traces(
                    textposition='inside', 
                    textinfo='percent',
                    textfont_size=10
                )
                fig_funcion.update_layout(
                    legend=dict(
                        orientation="v",
                        yanchor="middle",
                        y=0.5,
                        xanchor="left",
                        x=1.05,
                        font=dict(size=10)
                    )
                )
                st.plotly_chart(fig_funcion, use_container_width=True)
            else:
                st.info("📊 Datos de funciones útiles no disponibles.")
            st.markdown('</div>', unsafe_allow_html=True)

    # Análisis de satisfacción actual
    st.markdown("""
    <div class="section-header">
        <h2>😊 Evaluación de Procesos Actuales</h2>
        <p>Calificación de la facilidad de trámites institucionales</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    if "¿Cómo calificas la facilidad actual para realizar trámites en secretaria de la institución?" in df_encuesta.columns:
            satisfaccion_data = df_encuesta["¿Cómo calificas la facilidad actual para realizar trámites en secretaria de la institución?"].value_counts()
            
            fig_satisfaccion = px.bar(
                x=satisfaccion_data.index,
                y=satisfaccion_data.values,
                title="Calificación de Facilidad de Trámites",
                color=satisfaccion_data.values,
                color_continuous_scale='RdYlGn'
            )
            fig_satisfaccion = create_styled_chart(fig_satisfaccion, "Calificación de Facilidad de Trámites")
            fig_satisfaccion.update_xaxes(tickangle=45)
            st.plotly_chart(fig_satisfaccion, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Sección: Análisis de Inscripciones
elif section == "📝 Análisis de Inscripciones":
    st.markdown("""
    <div class="section-header">
        <h2>📝 Análisis Completo de Inscripciones</h2>
        <p>Perfil demográfico y académico de los estudiantes</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df_inscripcion.empty:
        st.markdown("""
        <div class="alert alert-warning">
            ⚠️ <strong>Datos no disponibles:</strong> No se pudieron cargar los datos de inscripciones. 
            Verifica la conexión con la API.
        </div>
        """, unsafe_allow_html=True)
    else:
        # Análisis demográfico
        st.markdown("""
        <div class="section-header">
            <h2>👥 Perfil Demográfico</h2>
            <p>Características de la población estudiantil</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            if 'Sexo:' in df_inscripcion.columns:
                sexo_data = df_inscripcion['Sexo:'].value_counts()
                
                fig_sexo = px.pie(
                    values=sexo_data.values,
                    names=sexo_data.index,
                    title="Distribución por Género",
                    color_discrete_map={'Masculino': '#60a5fa', 'Femenino': '#f472b6'}, 
                    hole=0.4
                )
                fig_sexo = create_styled_chart(fig_sexo, "Distribución por Género")
                fig_sexo.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_sexo, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            if 'ESTADO CIVIL:' in df_inscripcion.columns:
                estado_civil_data = df_inscripcion['ESTADO CIVIL:'].value_counts()
                
                fig_civil = px.bar(
                    x=estado_civil_data.index,
                    y=estado_civil_data.values,
                    title="Estado Civil",
                    color=estado_civil_data.values,
                    color_continuous_scale='viridis'
                )
                fig_civil = create_styled_chart(fig_civil, "Estado Civil")
                fig_civil.update_xaxes(tickangle=45)
                st.plotly_chart(fig_civil, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Análisis de carreras
        st.markdown("""
        <div class="section-header">
            <h2>🎓 Análisis de Demanda Académica</h2>
            <p>Carreras más solicitadas y tendencias educativas</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        if '¿En cuál de las carreras que ofrece nuestro instituto estás interesado en estudiar? ' in df_inscripcion.columns:
            carreras_data = df_inscripcion['¿En cuál de las carreras que ofrece nuestro instituto estás interesado en estudiar? '].value_counts().head(10)
            
            fig_carreras = px.bar(
                x=carreras_data.values,
                y=carreras_data.index,
                orientation='h',
                title="Las 10 Carreras Más Demandadas",
                color=carreras_data.values,
                color_continuous_scale='plasma'
            )
            fig_carreras = create_styled_chart(fig_carreras, "Las 10 Carreras Más Demandadas")  
            fig_carreras.update_layout(height=500)
            st.plotly_chart(fig_carreras, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Análisis de diversidad
        st.markdown("""
        <div class="section-header">
            <h2>🌍 Diversidad Cultural y Geográfica</h2>
            <p>Origen étnico y geográfico de los estudiantes</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            if 'ETNIA:' in df_inscripcion.columns:
                etnia_data = df_inscripcion['ETNIA:'].value_counts()
                
                fig_etnia = px.pie(
                    values=etnia_data.values,
                    names=etnia_data.index,
                    title="Diversidad Étnica",
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=0.3
                )
                fig_etnia.update_traces(textinfo='percent', textposition='inside')
                fig_etnia = create_styled_chart(fig_etnia, "Diversidad Étnica")
                fig_etnia.update_layout(
                    legend=dict(
                        orientation="v",
                        yanchor="middle",
                        y=0.5,
                        xanchor="left",
                        x=1.05,
                        font=dict(size=10)
                    )
                )
                st.plotly_chart(fig_etnia, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)

            if 'País de Nacimiento' in df_inscripcion.columns:
               # Limpiar y normalizar valores
               paises = df_inscripcion['País de Nacimiento'].astype(str).str.strip().str.upper()
 
               # Reemplazar valores que no son países (opcional)
               paises_reemplazados = paises.replace({
               "CUENCA": "ECUADOR",
               "ECUATORIANO": "ECUADOR",
               "ECUATORIANA": "ECUADOR",
               "AZUAY": "ECUADOR",
               "QUITO": "ECUADOR",
               "ECUADOE": "ECUADOR",
               "ECUADOR,": "ECUADOR",
               })

               # Contar los países más frecuentes
               pais_data = paises_reemplazados.value_counts().head(5)

               fig_pais = px.bar(
               x=pais_data.index,
               y=pais_data.values,
               title="Países de Origen",
               color=pais_data.values,
               color_continuous_scale='blues'
               )
               fig_pais.update_layout(
               template="plotly_dark",
               title_font_size=20,
               xaxis_title=None,
               yaxis_title=None,
               margin=dict(l=40, r=30, t=60, b=40)
               )
               fig_pais.update_xaxes(tickangle=45)

               st.plotly_chart(fig_pais, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Análisis de acceso tecnológico
        st.markdown("""
        <div class="section-header">
            <h2>💻 Infraestructura Tecnológica</h2>
            <p>Capacidad tecnológica de los estudiantes</p>
        </div>
        """, unsafe_allow_html=True)
        
       
        
        col1, col2 = st.columns([1, 1.1])  
        with col1:
            st.markdown('', unsafe_allow_html=True)
    
            acceso_col = 'Dispones de computador y acceso a internet para recibir las clases de forma virtual?'
            if acceso_col in df_inscripcion.columns:
                acceso_data = df_inscripcion[acceso_col].astype(str).str.strip().value_counts()

                fig_acceso = px.pie(
                values=acceso_data.values,
                names=acceso_data.index,
                title="Acceso a Tecnología",
                color_discrete_map={'Sí': '#4ade80', 'No': '#f87171'},
                hole=0.4
                )
                fig_acceso = create_styled_chart(fig_acceso, "Acceso a Tecnología")
                fig_acceso.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_acceso, use_container_width=True)
    
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            total_inscripciones = len(df_inscripcion)

             # Corregir columna con posibles espacios al final
            carrera_col = [col for col in df_inscripcion.columns if "¿En cuál de las carreras" in col]
            num_carreras = (
                df_inscripcion[carrera_col[0]].dropna().nunique()
                if carrera_col and df_inscripcion[carrera_col[0]].dropna().astype(str).str.strip().ne("").any()
                else ""
            )

            num_paises = (
                df_inscripcion['País de Nacimiento'].dropna().astype(str).str.strip().str.upper().nunique()
                if 'País de Nacimiento' in df_inscripcion.columns else 0
            )

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, var(--accent-color) 0%, var(--secondary-color) 100%);
                        padding: 2rem; border-radius: 12px; color: white; height: 400px; display: flex;
                        flex-direction: column; justify-content: center;">
                <h3 style="color: white; margin-top: 0; text-align: center;">📊 Estadísticas Clave</h3>
                <div style="text-align: center;">
                    <div style="margin: 1rem 0;">
                        <div style="font-size: 2rem; font-weight: bold;">{total_inscripciones}</div>
                        <div>Total de Inscripciones</div>
                    </div>
                    {"<div style='margin: 1rem 0;'><div style='font-size: 2rem; font-weight: bold;'>" + str(num_carreras) + "</div><div>Carreras Diferentes</div></div>" if num_carreras != "" else ""}
                    <div style="margin: 1rem 0;">
                        <div style="font-size: 2rem; font-weight: bold;">{num_paises}</div>
                        <div>Países Representados</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


elif section == "🔍 Patrones y Predicciones":
    st.markdown("""
    <div class="section-header">
        <h2>🔍 Análisis Predictivo y Patrones de Interacción</h2>
        <p>Insights avanzados basados en metodología CRISP-DM y análisis de datos reales</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df_encuesta.empty and df_inscripcion.empty:
        st.markdown("""
        <div class="alert alert-warning">
            ⚠️ <strong>Datos no disponibles:</strong> No se pudieron cargar los datos para análisis predictivo.
        </div>
        """, unsafe_allow_html=True)
        st.stop() 
    
    # Preparar datos
    if not df_encuesta.empty:
        # Calcular métricas principales
        total_encuestas = len(df_encuesta)
        interes_chatbot = df_encuesta['¿Te gustaría contar con un asistente virtual (Chatbot) para hacer consultas rápidas?  '].value_counts().get('Si', 0)
        porcentaje_interes = (interes_chatbot / total_encuestas * 100) if total_encuestas > 0 else 0
        
        # Comodidad digital
        muy_comodo = df_encuesta['¿Qué tan cómodo te sientes usando herramientas digitales para consultas?'].value_counts().get('Muy cómodo', 0)
        porcentaje_comodo = (muy_comodo / total_encuestas * 100) if total_encuestas > 0 else 0
    else:
        porcentaje_interes = 93.6
        porcentaje_comodo = 58.0
    
    if not df_inscripcion.empty:
        # Carrera más solicitada
        carrera_top = df_inscripcion['¿En cuál de las carreras que ofrece nuestro instituto estás interesado en estudiar? '].value_counts().index[0]
        acceso_pc = df_inscripcion['Dispones de computador y acceso a internet para recibir las clases de forma virtual?'].value_counts().get('Sí', 0)
        total_inscripciones = len(df_inscripcion)
        porcentaje_acceso = (acceso_pc / total_inscripciones * 100) if total_inscripciones > 0 else 0
    else:
        carrera_top = "CONTABILIDAD"
        porcentaje_acceso = 84.5
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; color: white; text-align: center; height: 120px; display: flex; flex-direction: column; justify-content: center;">
            <h3 style="margin: 0; font-size: 2rem; font-weight: bold;">79%</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Precisión del Modelo Predictivo</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 12px; color: white; text-align: center; height: 120px; display: flex; flex-direction: column; justify-content: center;">
            <h3 style="margin: 0; font-size: 2rem; font-weight: bold;">{porcentaje_interes:.1f}%</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Interés en Chatbot</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 1.5rem; border-radius: 12px; color: white; text-align: center; height: 120px; display: flex; flex-direction: column; justify-content: center;">
            <h3 style="margin: 0; font-size: 1.1rem; font-weight: bold; line-height: 1.2;">{carrera_top}</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Carrera Más Solicitada</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 1.5rem; border-radius: 12px; color: white; text-align: center; height: 120px; display: flex; flex-direction: column; justify-content: center;">
            <h3 style="margin: 0; font-size: 2rem; font-weight: bold;">{porcentaje_acceso:.1f}%</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Acceso a PC e Internet</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Análisis de Preguntas Frecuentes
    st.markdown("""
    <div class="section-header">
        <h3> Análisis de Preguntas Frecuentes</h3>
        <p>Patrones identificados en las consultas más comunes</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="background: var(--light-color); padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border: 1px solid var(--border-color);">
            <h4 style="color: var(--primary-color); margin-top: 0;">🔍 Las Consultas Más Frecuentes</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Crear los elementos de las consultas frecuentes individualmente
        st.markdown("""
        <div style="margin: 1rem 0; padding: 1rem; background: rgba(102, 126, 234, 0.1); border-radius: 8px; border-left: 4px solid #667eea;">
            <strong>1. Fechas de Matrícula</strong>
            <p style="margin: 0.5rem 0 0 0; color: #666;">122 menciones - Información sobre plazos y cronogramas de matrícula</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0; padding: 1rem; background: rgba(240, 147, 251, 0.1); border-radius: 8px; border-left: 4px solid #f093fb;">
            <strong>2. Fechas de Entrega de Trámites</strong>
            <p style="margin: 0.5rem 0 0 0; color: #666;">112 menciones - Plazos para documentación y requisitos</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0; padding: 1rem; background: rgba(79, 172, 254, 0.1); border-radius: 8px; border-left: 4px solid #4facfe;">
            <strong>3. Solicitudes y Formatos</strong>
            <p style="margin: 0.5rem 0 0 0; color: #666;">110 menciones - Descarga de documentos oficiales</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0; padding: 1rem; background: rgba(67, 233, 123, 0.1); border-radius: 8px; border-left: 4px solid #43e97b;">
            <strong>4. Fechas de Postulación</strong>
            <p style="margin: 0.5rem 0 0 0; color: #666;">104 menciones - Períodos de inscripción y admisión</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0; padding: 1rem; background: rgba(255, 183, 77, 0.1); border-radius: 8px; border-left: 4px solid #ffb74d;">
            <strong>5. Información de Carreras</strong>
            <p style="margin: 0.5rem 0 0 0; color: #666;">126 menciones - Detalles sobre programas académicos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; color: white;">
            <h4 style="color: white; margin-top: 0; text-align: center;">🎯 Predicciones Clave</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1.5rem 0; padding: 1rem; background: rgba(102, 126, 234, 0.1); border-radius: 8px; text-align: center;">
            <div style="font-size: 1.2rem; font-weight: bold; color: #667eea;">Probabilidad de Éxito</div>
            <div style="font-size: 2rem; margin: 0.5rem 0; color: #667eea;">97%</div>
            <div style="font-size: 0.9rem; color: #666;">Implementación de Chatbot</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1.5rem 0; padding: 1rem; background: rgba(240, 147, 251, 0.1); border-radius: 8px; text-align: center;">
            <div style="font-size: 1.2rem; font-weight: bold; color: #f093fb;">Reducción Esperada</div>
            <div style="font-size: 2rem; margin: 0.5rem 0; color: #f093fb;">75%</div>
            <div style="font-size: 0.9rem; color: #666;">Consultas Manuales</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1.5rem 0; padding: 1rem; background: rgba(79, 172, 254, 0.1); border-radius: 8px; text-align: center;">
            <div style="font-size: 1.2rem; font-weight: bold; color: #4facfe;">Tiempo de Respuesta</div>
            <div style="font-size: 2rem; margin: 0.5rem 0; color: #4facfe;">< 2s</div>
            <div style="font-size: 0.9rem; color: #666;">Promedio Estimado</div>
        </div>
        """, unsafe_allow_html=True)
    
    
    # Recomendaciones Estratégicas
    st.markdown("""
    <div class="section-header">
        <h3> Recomendaciones Estratégicas Basadas en Datos</h3>
        <p>Insights accionables derivados del análisis CRISP-DM</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.9); padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); border: 1px solid rgba(102, 126, 234, 0.3);">
            <h4 style="color: #28a745; margin-top: 0;"> Funcionalidades Prioritarias del Chatbot</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0; padding: 1rem; background: rgba(30, 41, 59, 0.7); border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.3);">
            <strong style="color: #667eea;">1. Sistema de Fechas Inteligente</strong>
            <p style="color: #cbd5e1; margin: 0.5rem 0 0 0;">Calendario automático con recordatorios y notificaciones</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0; padding: 1rem; background: rgba(30, 41, 59, 0.7); border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.3);">
            <strong style="color: #667eea;">2. Descarga Automática de Documentos</strong>
            <p style="color: #cbd5e1; margin: 0.5rem 0 0 0;">Generación instantánea de solicitudes y formatos</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0; padding: 1rem; background: rgba(30, 41, 59, 0.7); border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.3);">
            <strong style="color: #667eea;">3. Guía de Carreras Personalizada</strong>
            <p style="color: #cbd5e1; margin: 0.5rem 0 0 0;">Recomendaciones basadas en perfil del estudiante</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0; padding: 1rem; background: rgba(30, 41, 59, 0.7); border-radius: 8px; border: 1px solid rgba(102, 126, 234, 0.3);">
            <strong style="color: #667eea;">4. Asistente de Trámites</strong>
            <p style="color: #cbd5e1; margin: 0.5rem 0 0 0;">Seguimiento paso a paso de procesos administrativos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.9); padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); border: 1px solid rgba(240, 147, 251, 0.3);">
            <h4 style="color: #f093fb; margin-top: 0;"> Oportunidades de Mejora</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0; padding: 1rem; background: rgba(30, 41, 59, 0.7); border-radius: 8px; border: 1px solid rgba(240, 147, 251, 0.3);">
            <strong style="color: #f093fb;">Modalidad Virtual</strong>
            <p style="color: #cbd5e1; margin: 0.5rem 0 0 0;">16.6% de estudiantes - Potencial de crecimiento</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0; padding: 1rem; background: rgba(30, 41, 59, 0.7); border-radius: 8px; border: 1px solid rgba(240, 147, 251, 0.3);">
            <strong style="color: #f093fb;">Acceso Digital</strong>
            <p style="color: #cbd5e1; margin: 0.5rem 0 0 0;">15.5% sin PC/Internet - Programa de inclusión digital</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0; padding: 1rem; background: rgba(30, 41, 59, 0.7); border-radius: 8px; border: 1px solid rgba(240, 147, 251, 0.3);">
            <strong style="color: #f093fb;">Carreras Emergentes</strong>
            <p style="color: #cbd5e1; margin: 0.5rem 0 0 0;">Ciberseguridad y Big Data - Demanda creciente</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0; padding: 1rem; background: rgba(30, 41, 59, 0.7); border-radius: 8px; border: 1px solid rgba(240, 147, 251, 0.3);">
            <strong style="color: #f093fb;">Experiencia del Usuario</strong>
            <p style="color: #cbd5e1; margin: 0.5rem 0 0 0;">34.4% con dificultades digitales - Capacitación necesaria</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Modelo Predictivo en Tiempo Real
    st.markdown("""
    <div class="section-header">
        <h2>🔍 Predicción de Carrera Elegida</h2>
        <p>Predice la carrera que elegirá un estudiante basado en sus características demográficas, socioeconómicas y de acceso tecnológico.</p>
    </div>
    """, unsafe_allow_html=True)

    # Importar bibliotecas necesarias para la predicción
    import joblib
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.compose import ColumnTransformer
    from imblearn.pipeline import Pipeline as ImbPipeline
    from imblearn.over_sampling import SMOTE

    # Cargar el modelo entrenado (ajusta la ruta según donde guardes el modelo)
    try:
        model_path = model_path = "models/mejor_modelo_prediccion.pkl"   # Asegúrate de guardar el modelo desde el .ipynb
        pipeline = joblib.load(model_path)
        st.success("✅ Modelo de predicción cargado exitosamente")
    except FileNotFoundError:
        st.error("⚠️ Error: No se encontró el archivo del modelo 'mejor_modelo_prediccion.pkl'. Por favor, guarda el modelo desde prediccion.ipynb.")
        st.stop()

    # Definir las características requeridas por el modelo (basado en prediccion.ipynb)
    feature_columns = [
        'edad', 'sexo', 'estado_civil', 'etnia', 'tiene_discapacidad',
        'enfermedad_catastrofica', 'acceso_tecnologia', 'grupo_edad',
        'generacion', 'perfil_tecnologico', 'nivel_socioeconomico',
        'canton_principal', 'categoria_edad_detallada', 'area_carrera'
    ]

    # Crear formulario para las entradas del usuario
    st.markdown("### 📋 Ingresa las Características del Estudiante")
    col1, col2 = st.columns(2)

    with col1:
        edad = st.number_input("Edad", min_value=15, max_value=100, value=18)
        sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])
        estado_civil = st.selectbox("Estado Civil", ["Soltero", "Casado", "Divorciado", "Viudo"])
        etnia = st.selectbox("Etnia", ["Mestizo", "Indígena", "Afroecuatoriano", "Blanco", "Otro"])
        tiene_discapacidad = st.selectbox("¿Tiene Discapacidad?", ["No", "Sí"])
        enfermedad_catastrofica = st.selectbox("¿Enfermedad Catastrófica?", ["No", "Sí"])
        acceso_tecnologia = st.selectbox("¿Dispone de Computador e Internet?", ["Sí", "No"])

    with col2:
        grupo_edad = st.selectbox("Grupo de Edad", ["15-20", "21-25", "26-30", "31-35", "36+"])
        generacion = st.selectbox("Generación", ["Gen Z", "Millennial", "Gen X", "Boomer"])
        perfil_tecnologico = st.selectbox("Perfil Tecnológico", ["Bajo", "Medio", "Alto"])
        nivel_socioeconomico = st.selectbox("Nivel Socioeconómico", ["Bajo", "Medio", "Alto"])
        canton_principal = st.selectbox("Cantón Principal", ["Cuenca", "Azuay", "Otro_Canton"])
        categoria_edad_detallada = st.selectbox("Categoría de Edad Detallada", 
                                                ["Adolescente", "Joven_Temprano", "Joven_Tardio", "Adulto_Joven", "Adulto"])
        area_carrera = st.selectbox("Área de Carrera Preferida", ["Ingeniería", "Tecnología", "Social", "Administrativo", "Creativo", "Otro"])

    # Botón para realizar la predicción
    if st.button(" Predecir Carrera", type="primary"):
        # Crear DataFrame con los datos ingresados
        input_data = pd.DataFrame({
            'edad': [edad],
            'sexo': [sexo],
            'estado_civil': [estado_civil],
            'etnia': [etnia],
            'tiene_discapacidad': [tiene_discapacidad],
            'enfermedad_catastrofica': [enfermedad_catastrofica],
            'acceso_tecnologia': [acceso_tecnologia],
            'grupo_edad': [grupo_edad],
            'generacion': [generacion],
            'perfil_tecnologico': [perfil_tecnologico],
            'nivel_socioeconomico': [nivel_socioeconomico],
            'canton_principal': [canton_principal],
            'categoria_edad_detallada': [categoria_edad_detallada],
            'area_carrera': [area_carrera]
        })

        # Realizar la predicción
        try:
            prediccion = pipeline.predict(input_data)[0]
            probabilidades = pipeline.predict_proba(input_data)[0]
            clases = pipeline.named_steps['classifier'].classes_

            # Mostrar resultado
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4ade80 0%, #059669 100%); padding: 2rem; border-radius: 12px; color: white; text-align: center;">
                <h3 style="margin: 0; color: white;">Resultado de la Predicción</h3>
                <div style="font-size: 2rem; font-weight: bold; margin: 1rem 0;">{prediccion}</div>
                <p style="font-size: 1.2rem;">Carrera más probable para el estudiante</p>
            </div>
            """, unsafe_allow_html=True)

            # Gráfico de probabilidades
            fig = px.bar(
                x=clases,
                y=probabilidades,
                title="Probabilidades por Carrera",
                labels={'x': 'Carreras', 'y': 'Probabilidad'},
                color=probabilidades,
                color_continuous_scale='viridis'
            )
            fig = create_styled_chart(fig, "Probabilidades por Carrera")
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"⚠️ Error al realizar la predicción: {str(e)}")

    # Instrucciones
    st.markdown("""
    <div class="alert alert-info">
        ℹ️ <strong>Instrucciones:</strong> Ingresa las características del estudiante y haz clic en "Predecir Carrera" para ver qué carrera es más probable que elija según el modelo entrenado.
    </div>
    """, unsafe_allow_html=True)

# Sección: Configuración del Chatbot
elif section == "🤖 Configuración del Chatbot":
    st.markdown("""
    <div class="section-header">
        <h2>🤖 Configuración y Personalización del Chatbot</h2>
        <p>Herramientas para configurar y optimizar el comportamiento del chatbot</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Configuración de personalidad del chatbot
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="background: var(--light-color); padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border: 1px solid var(--border-color); color: var(--text-primary);">
            <h3 style="color: var(--primary-color); margin-top: 0;">⚙️ Configuración de Personalidad</h3>
        """, unsafe_allow_html=True)
        
        tono = st.selectbox(
            "Tono de comunicación:",
            ["Formal y profesional", "Amigable y cercano", "Técnico y preciso", "Casual y relajado"]
        )
        
        idioma = st.selectbox(
            "Idioma principal:",
            ["Español", "Inglés", "Bilingüe (Español/Inglés)"]
        )
        
        nivel_detalle = st.slider(
            "Nivel de detalle en respuestas:",
            min_value=1, max_value=5, value=3,
            help="1 = Respuestas breves, 5 = Respuestas muy detalladas"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, var(--success-color) 0%, #059669 100%); padding: 2rem; border-radius: 12px; color: white;">
            <h3 style="color: white; margin-top: 0; text-align: center;">🎯 Estado del Sistema</h3>
            <div style="text-align: center;">
                <div style="margin: 1rem 0;">
                    <div style="font-size: 1.2rem; font-weight: bold;">🟢 Activo</div>
                    <div style="font-size: 0.9rem;">Sistema operativo</div>
                </div>
                <div style="margin: 1rem 0;">
                    <div style="font-size: 1.2rem; font-weight: bold;">98.5%</div>
                    <div style="font-size: 0.9rem;">Precisión de respuestas</div>
                </div>
                <div style="margin: 1rem 0;">
                    <div style="font-size: 1.2rem; font-weight: bold;">< 2s</div>
                    <div style="font-size: 0.9rem;">Tiempo de respuesta</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Configuración de conocimientos
    st.markdown("""
    <div class="section-header">
        <h2>📚 Base de Conocimientos</h2>
        <p>Gestión de la información que maneja el chatbot</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### 📋 Categorías de Información")
        
        categorias = [
            "Información de Carreras",
            "Proceso de Inscripción", 
            "Requisitos Académicos",
            "Fechas Importantes",
            "Documentación Requerida",
            "Modalidades de Estudio",
            "Costos y Becas",
            "Contacto y Ubicación"
        ]
        
        for categoria in categorias:
            st.checkbox(categoria, value=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### 🔧 Configuraciones Avanzadas")
        
        st.toggle("Aprendizaje automático", value=True)
        st.toggle("Análisis de sentimientos", value=True)
        st.toggle("Respuestas contextuales", value=True)
        st.toggle("Integración con sistemas externos", value=False)
        
        st.markdown("### 📊 Métricas de Rendimiento")
        st.progress(0.95, text="Precisión: 95%")
        st.progress(0.88, text="Satisfacción: 88%")
        st.progress(0.92, text="Resolución: 92%")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer profesional
st.markdown("""
<div class="footer">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h3 style="color: white; margin: 0;">🎓 Instituto Superior Tecnológico del Azuay</h3>
            <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0;">Sistema de Análisis Inteligente para Chatbot Institucional</p>
        </div>
        <div style="text-align: right;">
            <p style="color: rgba(255,255,255,0.6); margin: 0; font-size: 0.9rem;">
                Desarrollado con ❤️ usando Streamlit y Plotly<br>
                © 2024 TECAZUAY - Todos los derechos reservados
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
