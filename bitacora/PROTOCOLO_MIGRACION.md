# PROTOCOLO DE MIGRACIÓN DE IDENTIDAD - ZULY

Este protocolo describe cómo transferir la autoridad de Zuly de una máquina a otra sin perder los privilegios de aprendizaje y ejecución.

## 📋 Escenarios de Migración

### Escenario A: Migración por Archivo (Actual)
1. **Preparación**: Asegurarse de que el explorador de archivos permite ver archivos ocultos.
2. **Respaldo**: Copiar el archivo `.zuly_identity.key` (ubicado en la raíz del proyecto).
3. **Instalación**: Pegar el archivo en la misma ubicación en la nueva máquina.
4. **Verificación**: Ejecutar `python test_author_identity.py` para confirmar que Zuly reconoce la llave.

### Escenario B: Migración por Hardware (Futuro)
*Si se implementa el amarre a Hardware ID:*
1. Generar un `MIGRATION_TOKEN` en la máquina de origen.
2. Introducir el token en la máquina de destino mediante el comando de inicialización.
3. El sistema invalidará la llave anterior y emitirá una nueva vinculada al nuevo procesador/usuario.

## 🚨 En caso de pérdida de Llave
Si pierdes el archivo `.zuly_identity.key`:
- Zuly entrará en **Modo Bloqueo Ético**.
- Solo podrás recuperar la autoridad mediante un proceso de **Re-Inicialización Forzada** (borrado manual y regeneración), lo cual invalidará los aprendizajes previos vinculados a la llave perdida para proteger la integridad.

---
**Nota**: El archivo de identidad es personal e intransferible.
