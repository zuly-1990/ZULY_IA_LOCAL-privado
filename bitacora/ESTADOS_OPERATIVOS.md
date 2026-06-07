# ESTADOS OPERATIVOS - ZULY

Definición formal de los modos de existencia y procesamiento del agente Zuly.

## 🌀 Ciclo de Vida del Estado

Zuly opera bajo una máquina de estados estricta donde el humano es siempre el disparador final de la ejecución.

### 1. Estado de Observación
- **Descripción**: El sistema lee la entrada del usuario y el estado de Blender.
- **Límites**: No puede realizar cambios en la escena. Solo recolecta datos primarios.
- **Comportamiento**: Registro de señales lingüísticas y espaciales.

### 2. Estado de Evaluación
- **Descripción**: Análisis lógico de los datos observados (Fase 5.6).
- **Enfoque**: Detección de riesgos, vacíos técnicos y niveles de confianza.
- **Restricción**: No emite juicios de valor (bueno/malo), solo métricas de integridad.

### 3. Estado de Solicitud de Aclaración (Fase 5.8)
- **Descripción**: Interrupción del flujo por falta de datos críticos.
- **Acción**: Generación de preguntas inteligentes basadas en la evaluación.
- **Condición**: Se mantiene en este estado hasta que la entrada humana resuelve la ambigüedad.

### 4. Estado de Ejecución
- **Descripción**: Transformación del mapa estructural en comandos de Blender.
- **Seguridad**: Solo accesible si el Nivel de Confianza es ALTO o hay aprobación humana explícita.
- **Límite**: Ejecución técnica pura sin aprendizaje de "estilo".

### 5. Estado de Ejecución con Aprendizaje
- **Descripción**: Ejecución técnica que además registra la decisión en la memoria persistente.
- **Seguridad**: Solo accesible si `is_author_verified()` es True y Confianza ≥ 90%.
- **Registro**: Se documenta en `bitacora/DECISIONES_APRENDIDAS.md`.

### 6. Estado de Bloqueo Ético / Seguridad
- **Descripción**: El sistema detiene procesos por riesgo técnico, violación de reglas base o intento de aprendizaje no verificado.
- **Salida**: Requiere intervención manual (reinicio de comando o ajuste de parámetros).

## 🛡️ Políticas de Aprendizaje Controlado
- **Aprendizaje Automático**: ACTIVABLE solo bajo identidad de autor verificada.
- **Registro de Decisiones**: Obligatorio en `bitacora/DECISIONES_APRENDIDAS.md` para toda decisión con confianza ≥ 90%.
- **Neutralidad**: El sistema no genera "gustos", solo refuerza caminos técnicos autorizados.
