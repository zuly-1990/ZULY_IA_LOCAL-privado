import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Zuly Dashboard", page_icon="🧠", layout="wide")

st.title("🧠 Zuly - Web Dashboard de Monitoreo")
st.markdown("Visualización en tiempo real del Cerebro Cognitivo de Zuly.")

# Funciones de carga de datos
@st.cache_data(ttl=5)
def load_patterns():
    db_path = "bitacora/patterns_signed.db"
    if not os.path.exists(db_path):
        return pd.DataFrame()
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT pattern_name, pattern_type, score_final, confianza, uses_count, timestamp_firma FROM patterns_signed", conn)
    conn.close()
    return df

@st.cache_data(ttl=5)
def load_experiences():
    db_path = "bitacora/memory.db"
    if not os.path.exists(db_path):
        return pd.DataFrame()
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT objective, evaluation_score, metrics_passed, metrics_total, timestamp FROM experiences", conn)
    conn.close()
    return df

# Cargar datos
df_patterns = load_patterns()
df_experiences = load_experiences()

# Pestañas
tab1, tab2, tab3 = st.tabs(["📊 Métricas Globales", "🧠 C2 Memory (Patrones)", "⚙️ Configuración"])

with tab1:
    st.header("Métricas de Rendimiento y Experiencia")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Patrones Consolidados", value=len(df_patterns) if not df_patterns.empty else 0)
    with col2:
        st.metric(label="Experiencias (Evaluaciones)", value=len(df_experiences) if not df_experiences.empty else 0)
    with col3:
        avg_score = df_patterns['score_final'].mean() if not df_patterns.empty else 0
        st.metric(label="Score Promedio (C1)", value=f"{avg_score:.2f}%")

    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Experiencias por Evaluación")
        if not df_experiences.empty:
            df_experiences['timestamp'] = pd.to_datetime(df_experiences['timestamp'])
            df_experiences = df_experiences.sort_values(by='timestamp')
            fig1 = px.line(df_experiences, x='timestamp', y='evaluation_score', title="Puntuación a lo largo del tiempo", markers=True)
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No hay experiencias registradas en memory.db")

    with col_chart2:
        st.subheader("Distribución de Patrones por Tipo")
        if not df_patterns.empty:
            fig2 = px.pie(df_patterns, names='pattern_type', title="Tipos de Patrones")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No hay patrones registrados en patterns_signed.db")

with tab2:
    st.header("Explorador de C2 Memory (Memoria a Largo Plazo)")
    
    if not df_patterns.empty:
        st.dataframe(
            df_patterns.style.highlight_max(axis=0, subset=['score_final', 'uses_count']),
            use_container_width=True,
            height=400
        )
    else:
        st.warning("La base de datos de patrones está vacía o no se encuentra.")

with tab3:
    st.header("Estado de los Módulos Base")
    st.write("✅ C1_Evaluador en línea")
    st.write("✅ C2_Memory en línea")
    st.write("✅ C3_Task_Decomposer en línea")
    st.write("✅ SafeGuard Integrado")
