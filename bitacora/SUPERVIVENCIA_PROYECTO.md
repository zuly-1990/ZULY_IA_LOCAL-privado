# PLAN DE SUPERVIVENCIA Y CONTINUIDAD - ZULY

¡Esta es la 6ta versión y será la definitiva! Para evitar que el proyecto se pierda de nuevo, implementamos este protocolo de "Cero Pérdidas".

## 🛡️ Estrategia de Triple Respaldo

### 1. Respaldo Local Automatizado (El "Seguro de Vida")
- **Herramienta**: Script `herramientas/backup_zuly.ps1`.
- **Frecuencia**: Ejecutar al final de cada sesión de trabajo.
- **Qué guarda**: Todo el proyecto, incluidos archivos ocultos como `.zuly_identity.key` y la base de datos de conocimiento.

### 2. Respaldo del Entorno (La "Receta de Cocina")
- **requirements.txt**: Mantiene la lista exacta de librerías. Si se borra la carpeta `.venv`, se reinstala en 2 minutos.
- **Guía de Inicio**: Documento `INICIO_AQUI.txt` con los pasos exactos para revivir a Zuly desde cero.

### 3. Respaldo de Identidad (La "Llave Maestra")
- **IMPORTANTE**: Copia el archivo `.zuly_identity.key` en un lugar ajeno a la carpeta del proyecto (USB, correo personal, etc.). Sin esto, Zuly entrará en bloqueo ético.

## 🚨 Protocolo de Recuperación (En caso de desastre)

1. **Si Windows falla**: Reinstala Python 3.10+ y Blender.
2. **Si la carpeta se borra**: Descarga tu último respaldo ZIP.
3. **Reconstrucción**:
   - Abre la carpeta en VS Code.
   - Ejecuta `python -m venv .venv`.
   - Ejecuta `.venv\Scripts\activate`.
   - Ejecuta `pip install -r requirements.txt`.
4. **Verificación**: Corre `python test_author_identity.py`. Si todo está verde, Zuly ha vuelto a la vida.

---
> [!TIP]
> No confíes solo en una carpeta en el escritorio. Usa el script de respaldo para generar un archivo ZIP fechado cada vez que logremos un hito importante.
