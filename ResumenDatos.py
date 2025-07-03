import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Cargar datos desde archivos Excel
df1 = pd.read_excel(r"C:\Users\VivoBook\Downloads\Proyecto Chat Bot\Inscripción ImpulsaT - TECAZUAY (respuestas) (1).xlsx")
df2 = pd.read_excel(r"C:\Users\VivoBook\Downloads\Proyecto Chat Bot\Encuesta para el proyecto _Asistente Institucional_  (respuestas).xlsx")

# Configuración de la página
st.set_page_config(
    page_title="Dashboard - Chatbot Institucional",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado mejorado para un diseño más moderno
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 3rem;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(226, 232, 240, 0.8);
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-delta {
        font-size: 0.8rem;
        color: #10b981;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .section-header {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 3rem 0 2rem 0;
        font-weight: 600;
        color: #1e293b;
        border-left: 6px solid #667eea;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        font-size: 1.4rem;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .insight-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    }
    
    .insight-box h3 {
        color: #1e293b;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    
    .insight-box ul {
        list-style: none;
        padding: 0;
    }
    
    .insight-box li {
        padding: 0.8rem 0;
        border-bottom: 1px solid #f1f5f9;
        color: #475569;
        line-height: 1.6;
    }
    
    .insight-box li:last-child {
        border-bottom: none;
    }
    
    .insight-box strong {
        color: #3b82f6;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: #ffffff;
        border-radius: 12px;
        color: #64748b;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f8fafc;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }
    
    .chart-container {
        background: #ffffff;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid #f1f5f9;
        margin: 1rem 0;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-item {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .stat-item:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.12);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #3b82f6;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 500;
    }
    
    .footer {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        text-align: center;
        padding: 3rem 2rem;
        margin-top: 4rem;
        border-radius: 20px 20px 0 0;
    }
    
    .footer p {
        margin: 0.5rem 0;
        opacity: 0.9;
    }
    
    /* Animaciones personalizadas */
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-slide-up {
        animation: slideInUp 0.6s ease-out;
    }
    
    /* Responsive design mejorado */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .metric-card {
            padding: 1.5rem;
        }
        
        .section-header {
            font-size: 1.2rem;
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Cargar datos (usando datos simulados para la demostración)
@st.cache_data
def load_data():
    # Simular datos basados en las columnas proporcionadas
    np.random.seed(42)
    n_inscripciones = 250
    n_encuestas = 180
    
    # DataFrame 1: Inscripciones
    df1_sim = pd.DataFrame({
        'Sexo:': np.random.choice(['Masculino', 'Femenino'], n_inscripciones, p=[0.45, 0.55]),
        'ESTADO CIVIL:': np.random.choice(['Soltero', 'Casado', 'Unión libre', 'Divorciado'], n_inscripciones, p=[0.6, 0.25, 0.1, 0.05]),
        'ETNIA:': np.random.choice(['Mestizo', 'Indígena', 'Blanco', 'Afroecuatoriano'], n_inscripciones, p=[0.7, 0.15, 0.1, 0.05]),
        '¿En cuál de las carreras que ofrece nuestro instituto estás interesado en estudiar? ': np.random.choice([
            'Desarrollo de Software', 'Marketing Digital', 'Contabilidad', 'Administración', 'Diseño Gráfico'
        ], n_inscripciones, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
        'Dispones de computador y acceso a internet para recibir las clases de forma virtual?': np.random.choice(['Sí', 'No'], n_inscripciones, p=[0.85, 0.15])
    })
    
    # DataFrame 2: Encuesta sobre chatbot
    df2_sim = pd.DataFrame({
        '¿Cuál es tu modalidad de estudios?  ': np.random.choice(['Presencial', 'Virtual', 'Semipresencial'], n_encuestas, p=[0.5, 0.3, 0.2]),
        '¿Con qué frecuencia necesitas información de Secretaría?': np.random.choice(['Diariamente', 'Semanalmente', 'Mensualmente', 'Ocasionalmente'], n_encuestas, p=[0.15, 0.35, 0.3, 0.2]),
        '¿Te gustaría contar con un asistente virtual (Chatbot) para hacer consultas rápidas?  ': np.random.choice(['Sí', 'No', 'Tal vez'], n_encuestas, p=[0.75, 0.1, 0.15]),
        '¿Qué tan cómodo te sientes usando herramientas digitales para consultas?': np.random.choice(['Muy cómodo', 'Cómodo', 'Neutral', 'Incómodo'], n_encuestas, p=[0.4, 0.35, 0.2, 0.05]),
        '¿Cómo calificas la facilidad actual para realizar trámites en secretaria de la institución?': np.random.choice(['Muy fácil', 'Fácil', 'Regular', 'Difícil', 'Muy difícil'], n_encuestas, p=[0.1, 0.25, 0.4, 0.2, 0.05])
    })
    
    return df1_sim, df2_sim

# Cargar datos
df1, df2 = load_data()

# Header principal mejorado
st.markdown("""
<div class="main-header animate-slide-up">
    <h1>🤖 Dashboard Inteligente</h1>
    <p>Análisis Integral para la Implementación del Chatbot Institucional</p>
</div>
""", unsafe_allow_html=True)

# Métricas principales mejoradas
st.markdown('<div class="animate-slide-up">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">250</div>
        <div class="metric-label">Total Inscripciones</div>
        <div class="metric-delta">📈 +15% vs mes anterior</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">180</div>
        <div class="metric-label">Encuestas Completadas</div>
        <div class="metric-delta">✅ 72% tasa de respuesta</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    acceptance = 75.0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{acceptance}%</div>
        <div class="metric-label">Aceptación Chatbot</div>
        <div class="metric-delta">🎯 Alta demanda estudiantil</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">5</div>
        <div class="metric-label">Carreras Disponibles</div>
        <div class="metric-delta">📚 Amplia oferta académica</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Tabs mejorados
tab1, tab2, tab3 = st.tabs(["👥 Perfil Estudiantil", "🤖 Necesidad del Chatbot", "📊 Insights & ROI"])

with tab1:
    st.markdown('<div class="section-header">👥 Análisis Demográfico Completo</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        if 'Sexo:' in df1.columns:
            fig_gender = px.pie(df1, names='Sexo:', title="Distribución por Género",
                              color_discrete_sequence=['#667eea', '#764ba2'],
                              hole=0.4)
            fig_gender.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                textfont_size=12,
                marker=dict(line=dict(color='#FFFFFF', width=2))
            )
            fig_gender.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12, family="Inter"),
                title_font_size=16,
                title_font_color='#1e293b',
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            st.plotly_chart(fig_gender, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        if 'ESTADO CIVIL:' in df1.columns:
            civil_counts = df1['ESTADO CIVIL:'].value_counts().reset_index()
            civil_counts.columns = ['Estado_Civil', 'Cantidad']
            fig_civil = px.bar(civil_counts,
                             x='Estado_Civil', y='Cantidad', 
                             title="Estado Civil de Estudiantes",
                             color='Cantidad', 
                             color_continuous_scale='Viridis',
                             text='Cantidad')
            fig_civil.update_traces(texttemplate='%{text}', textposition='outside')
            fig_civil.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                xaxis_title="Estado Civil",
                yaxis_title="Cantidad",
                font=dict(size=12, family="Inter"),
                title_font_size=16,
                title_font_color='#1e293b'
            )
            st.plotly_chart(fig_civil, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Estadísticas adicionales
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-item">
            <div class="stat-number">85%</div>
            <div class="stat-label">Con acceso a internet</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">60%</div>
            <div class="stat-label">Estudiantes solteros</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">70%</div>
            <div class="stat-label">Etnia mestiza</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">30%</div>
            <div class="stat-label">Interés en Software</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Gráfico de carreras mejorado
    if '¿En cuál de las carreras que ofrece nuestro instituto estás interesado en estudiar? ' in df1.columns:
        st.markdown('<div class="section-header">🎓 Demanda por Programas Académicos</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        career_counts = df1['¿En cuál de las carreras que ofrece nuestro instituto estás interesado en estudiar? '].value_counts()
        career_df = pd.DataFrame({
            'Carrera': career_counts.index,
            'Cantidad': career_counts.values,
            'Porcentaje': (career_counts.values / career_counts.sum() * 100).round(1)
        })
        
        fig_careers = px.bar(
            career_df,
            x='Cantidad',
            y='Carrera',
            orientation='h',
            title="Interés por Carreras Ofertadas",
            color='Cantidad',
            color_continuous_scale='Plasma',
            text='Porcentaje'
        )
        fig_careers.update_traces(
            texttemplate='%{text}%', 
            textposition='inside',
            textfont_color='white',
            textfont_size=12
        )
        fig_careers.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            xaxis_title="Número de Estudiantes Interesados",
            yaxis_title="Programas Académicos",
            font=dict(size=12, family="Inter"),
            title_font_size=16,
            title_font_color='#1e293b'
        )
        st.plotly_chart(fig_careers, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-header">🤖 Justificación Técnica del Chatbot</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        if '¿Con qué frecuencia necesitas información de Secretaría?' in df2.columns:
            freq_data = df2['¿Con qué frecuencia necesitas información de Secretaría?'].value_counts()
            fig_freq = px.pie(values=freq_data.values, names=freq_data.index,
                            title="Frecuencia de Consultas a Secretaría",
                            color_discrete_sequence=px.colors.qualitative.Set3,
                            hole=0.5)
            fig_freq.update_traces(
                textposition='auto', 
                textinfo='percent+label',
                textfont_size=11,
                marker=dict(line=dict(color='#FFFFFF', width=2))
            )
            fig_freq.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12, family="Inter"),
                title_font_size=16,
                title_font_color='#1e293b',
                showlegend=True,
                legend=dict(orientation="v", yanchor="middle", y=0.5, x=1.1)
            )
            st.plotly_chart(fig_freq, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        if '¿Te gustaría contar con un asistente virtual (Chatbot) para hacer consultas rápidas?  ' in df2.columns:
            chatbot_acceptance = df2['¿Te gustaría contar con un asistente virtual (Chatbot) para hacer consultas rápidas?  '].value_counts()
            acceptance_df = pd.DataFrame({
                'Respuesta': chatbot_acceptance.index,
                'Cantidad': chatbot_acceptance.values
            })
            fig_acceptance = px.bar(
                acceptance_df,
                x='Respuesta',
                y='Cantidad',
                title="Nivel de Aceptación del Chatbot",
                color='Cantidad',
                color_continuous_scale='RdYlGn',
                text='Cantidad'
            )
            fig_acceptance.update_traces(texttemplate='%{text}', textposition='outside')
            fig_acceptance.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Respuesta de Estudiantes",
                yaxis_title="Cantidad",
                font=dict(size=12, family="Inter"),
                title_font_size=16,
                title_font_color='#1e293b'
            )
            st.plotly_chart(fig_acceptance, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Panel de métricas clave
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-item">
            <div class="stat-number">50%</div>
            <div class="stat-label">Consulta semanalmente</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">75%</div>
            <div class="stat-label">Quiere chatbot</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">75%</div>
            <div class="stat-label">Cómodo con digital</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">65%</div>
            <div class="stat-label">Trámites difíciles</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Análisis de comodidad digital
    if '¿Qué tan cómodo te sientes usando herramientas digitales para consultas?' in df2.columns:
        st.markdown('<div class="section-header">💻 Readiness Digital de Estudiantes</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        digital_comfort = df2['¿Qué tan cómodo te sientes usando herramientas digitales para consultas?'].value_counts()
        comfort_df = pd.DataFrame({
            'Nivel_Comodidad': digital_comfort.index,
            'Cantidad': digital_comfort.values
        })
        
        fig_comfort = px.bar(
            comfort_df,
            x='Nivel_Comodidad',
            y='Cantidad',
            title="Nivel de Comodidad con Herramientas Digitales",
            color='Cantidad',
            color_continuous_scale='Blues',
            text='Cantidad'
        )
        fig_comfort.update_traces(texttemplate='%{text}', textposition='outside')
        fig_comfort.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            font=dict(size=12, family="Inter"),
            title_font_size=16,
            title_font_color='#1e293b'
        )
        st.plotly_chart(fig_comfort, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


    
