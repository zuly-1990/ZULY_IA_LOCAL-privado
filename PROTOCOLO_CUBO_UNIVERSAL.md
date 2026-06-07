# Protocolo Cubo Universal

## Objetivo
Establecer un estándar de automatización, renderizado y análisis para pruebas 3D con cubos en Blender, adaptable a cualquier entorno (local, nube, multiplataforma).

## Alcance
- Creación, animación y renderizado de cubos con diferentes colores, posiciones y animaciones.
- Organización y registro de resultados (imágenes, .blend, logs).
- Scripts portables y parametrizables.
- Base para futuras expansiones (nodos, IA, interfaz web, add-on, cloud).

## Estructura del protocolo
1. **Generación de cubos**
   - Color, tamaño, posición y cantidad parametrizables.
   - Materiales y animaciones básicas (rotación, aparición/desaparición).
2. **Automatización de cámara y luces**
   - Posición y orientación inteligente de cámara.
   - Iluminación ajustable para visibilidad óptima.
3. **Renderizado y exportación**
   - Render en secuencia de imágenes y guardado de .blend.
   - Organización en carpetas por prueba y fecha.
4. **Análisis de resultados**
   - Scripts para analizar imágenes (brillo, contraste, visibilidad).
   - Logs de parámetros y resultados.
5. **Portabilidad y documentación**
   - Uso de rutas relativas.
   - requirements.txt y README para migración.

## Ejemplo de flujo
1. Ejecutar script de prueba (ej: cubo amarillo rotando).
2. Renderizar y guardar resultados.
3. Analizar imágenes generadas.
4. Registrar parámetros y resultados en log.

## Estado actual
- Scripts de generación y animación de cubos funcionales.
- Render y análisis básico implementados.
- Organización de archivos y carpetas lista.

## Próximos pasos
- Mejorar autoajuste de cámara y luz.
- Añadir más tipos de animaciones y materiales.
- Integrar análisis avanzado y feedback.
- Preparar para integración con interfaz web y cloud.

---

Este documento es el registro oficial del Protocolo Cubo Universal. Cualquier mejora o expansión futura debe documentarse aquí antes de pasar al Protocolo Libre Albedrío.