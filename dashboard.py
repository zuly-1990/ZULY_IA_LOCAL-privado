import streamlit as st
import psutil
import pandas as pd
import os
from datetime import datetime
import time

st.set_page_config(page_title="Zuly Monitor Dashboard", page_icon="🏗️", layout="wide")

st.title("🏗️ Zuly Autonomous Monitor - Hetzner Node")
st.markdown("Dashboard en vivo para monitoreo de Blender, Nodos de Geometría y Salud del Servidor.")

# --- SIDEBAR ---
st.sidebar.header("Estado del Demonio")
try:
    status_cmd = os.popen('systemctl is-active zuly_tutor.service').read().strip()
    if status_cmd == "active":
        st.sidebar.success("🟢 Zuly Tutor: ACTIVO (Running)")
    else:
        st.sidebar.error(f"🔴 Zuly Tutor: INACTIVO ({status_cmd})")
except Exception:
    st.sidebar.warning("⚠️ Zuly Tutor: Estado Desconocido")

# --- ROW 1: METRICS ---
col1, col2, col3 = st.columns(3)

cpu_usage = psutil.cpu_percent(interval=0.1)
ram_usage = psutil.virtual_memory().percent
disk_usage = psutil.disk_usage('/').percent

col1.metric("CPU Server", f"{cpu_usage}%")
col2.metric("RAM Server", f"{ram_usage}%", "Crítico si > 85%", delta_color="inverse")
col3.metric("Disco SSD", f"{disk_usage}%")

# --- ROW 2: GENERATED FILES ---
st.subheader("📁 Archivos .blend Generados")
zuly_dir = "/opt/zuly"
blend_files = []
if os.path.exists(zuly_dir):
    for f in os.listdir(zuly_dir):
        if f.endswith(".blend"):
            filepath = os.path.join(zuly_dir, f)
            stat = os.stat(filepath)
            blend_files.append({
                "Archivo": f,
                "Tamaño (KB)": round(stat.st_size / 1024, 2),
                "Última Modificación": datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })

if blend_files:
    df_files = pd.DataFrame(blend_files).sort_values(by="Última Modificación", ascending=False)
    st.dataframe(df_files, use_container_width=True)
else:
    st.info("No se encontraron archivos .blend en el directorio.")

# --- ROW 3: LOGS ---
st.subheader("📜 Consola en Vivo (weekend_autorepair.log)")

def read_logs():
    log_path = "/opt/zuly/bitacora/weekend_autorepair.log"
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return "".join(lines[-20:])
    return "No hay logs disponibles."

log_placeholder = st.empty()
log_placeholder.code(read_logs(), language="bash")

if st.button("🔄 Actualizar Dashboard"):
    st.rerun()
