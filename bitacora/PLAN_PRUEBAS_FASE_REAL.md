# **PLAN INTEGRAL DE PRUEBAS REALES - ZULY 4.0**

**Fecha:** 7 de diciembre de 2025  
**Estado:** En ejecución  
**Objetivo:** Validar que ZULY 4.0 es completamente funcional en todas sus capas  

---

## **1. ESTRATEGIA GENERAL DE PRUEBAS**

### **Niveles de Pruebas (Pirámide de Testing)**

```
                    ▲
                   / \
                  /   \  E2E (End-to-End)
                 /     \  - Flujos completos
                /-------\
               /         \ Integración
              /           \ - Módulos interactuando
             /             \
            /_______________\ Unitarias
            - Funciones      - Clases
            - Métodos        - Módulos aislados
```

### **Matriz de Pruebas**

| Nivel | Cantidad | Herramientas | Tiempo Est. |
|-------|----------|------------|------------|
| **Unitarias** | 45+ tests | unittest, pytest | 15 min |
| **Integración** | 20+ tests | unittest + mocks | 20 min |
| **E2E** | 15+ tests | Blender API real | 45 min |
| **Sistema** | 10+ tests | Web UI + Blender | 60 min |
| **Total** | 90+ tests | Multi-tool | ~2.5 horas |

---

## **2. PRUEBAS UNITARIAS (Nivel Base)**

### **2.1 Módulo: NLU (core/utils/nlu.py)**

**Objetivo:** Validar interpretación correcta de comandos naturales

**Tests:**
```
✓ test_nlu_crear_cubo_basico
  - Input: "crea un cubo"
  - Output: CommandIntent(type='crear_primitiva', params={'tipo': 'cubo'})

✓ test_nlu_render_con_parametros
  - Input: "renderiza con 128 muestras"
  - Output: CommandIntent con samples=128

✓ test_nlu_comandos_multiidioma
  - Input: "create cube" (en) + "crear cubo" (es)
  - Output: Ambos generan el mismo intent

✓ test_nlu_parametros_malformados
  - Input: "cubo con -999 muestras"
  - Output: Error controlado o default

✓ test_nlu_fuzzy_matching
  - Input: "krea un cubu" (typo)
  - Output: Reconoce como "crear cubo"
```

### **2.2 Módulo: Commands (core/commands/)**

**Objetivo:** Validar que cada comando funciona en aislamiento

**Tests por comando:**
```
✓ test_CrearPrimitiva_valido
✓ test_CrearPrimitiva_parametros_invalidos
✓ test_AplicarMaterial_colores_validos
✓ test_AplicarMaterial_colores_invalidos
✓ test_Renderizar_configuracion_basica
✓ test_Renderizar_con_custom_samples
✓ test_AplicarBevel_parametros
✓ test_SubdivisionSurface_valido
✓ test_Boolean_operaciones
```

### **2.3 Módulo: Agent (core/agent.py)**

**Objetivo:** Validar lógica central del agente

**Tests:**
```
✓ test_agent_initialization
✓ test_agent_command_loading
✓ test_agent_execute_single_command
✓ test_agent_context_persistence
✓ test_agent_error_handling
✓ test_agent_scene_monitoring
```

### **2.4 Módulo: Asset Library (core/assets/asset_library.py)**

**Objetivo:** Validar gestión de assets

**Tests:**
```
✓ test_asset_library_initialization
✓ test_asset_search_by_name
✓ test_asset_search_by_category
✓ test_asset_import_valido
✓ test_asset_persistence_json
✓ test_asset_deduplication
```

### **2.5 Módulo: Multi-language (core/utils/multilanguage.py)**

**Objetivo:** Validar soporte multiidioma

**Tests:**
```
✓ test_translation_es_to_en
✓ test_translation_es_to_fr
✓ test_nlu_keyword_es
✓ test_nlu_keyword_en
✓ test_language_switching
✓ test_missing_translation_fallback
```

---

## **3. PRUEBAS DE INTEGRACIÓN (Nivel Intermedio)**

### **3.1 NLU → Commands**

**Objetivo:** Validar flujo desde texto natural a ejecución

```
Test: test_nlu_to_command_pipeline
  1. Input: "crea una esfera roja con 64 muestras"
  2. NLU interpreta → CommandIntent
  3. Agent carga comando
  4. Comando ejecuta
  5. Scene monitor captura cambios
  6. Assert: Esfera existe, es roja, render tiene 64 samples
```

### **3.2 Commands → Asset Library**

**Objetivo:** Validar que comandos usan assets correctamente

```
Test: test_import_asset_and_use
  1. Asset library carga asset "cubo_dorado.blend"
  2. Comando "AplicarMaterial" lo referencia
  3. Material se aplica correctamente
  4. Assert: Asset se importó sin errores
```

### **3.3 Web UI → Agent → Commands**

**Objetivo:** Validar comunicación WebSocket

```
Test: test_websocket_command_execution
  1. Cliente Web envía: {"command": "crear_cubo"}
  2. Socket recibe y enruta a Agent
  3. Agent ejecuta comando
  4. Socket emite resultado
  5. Assert: Cliente recibe respuesta validada
```

### **3.4 Animation Engine → Rendering**

**Objetivo:** Validar pipeline de animaciones

```
Test: test_animation_rendering_pipeline
  1. AnimationBuilder crea keyframes
  2. Renderer genera frames
  3. FFmpeg genera video
  4. Assert: Archivo MP4 existe y es válido
```

---

## **4. PRUEBAS END-TO-END (Nivel Alto)**

### **Escenario 1: Crear y Renderizar Objeto**

```
E2E Test: test_complete_create_render_flow

Precondiciones:
  - Blender 3.6+ instalado
  - Proyecto limpio

Pasos:
  1. Agent.execute("crea un cubo de 2x2x2")
     → Cubo creado, escala = 2,2,2
  
  2. Agent.execute("aplica material oro")
     → Material oro aplicado
  
  3. Agent.execute("renderiza con 256 muestras")
     → Archivo render.png generado
  
  4. VisionAnalyzer analiza imagen
     → Detecta cubo, material dorado
  
Aserciones:
  ✓ Archivo render existe
  ✓ Imagen tiene dimensiones > 0
  ✓ Cubo visible en imagen
  ✓ Color oro detectado
```

### **Escenario 2: Secuencia de Modificadores**

```
E2E Test: test_modifier_sequence

Pasos:
  1. Crear primitiva: cilindro
  2. Aplicar Bevel: amount=0.1
  3. Aplicar Subdivision: levels=2
  4. Aplicar Mirror: eje X
  5. Renderizar
  
Aserciones:
  ✓ Todos los modificadores aplicados
  ✓ Geometría correcta
  ✓ Render sin errores
```

### **Escenario 3: Animación Completa**

```
E2E Test: test_animation_full_workflow

Pasos:
  1. Crear cubo
  2. AnimationBuilder: rotación 360° en 120 frames
  3. AnimationBuilder: camera zoom
  4. Render animación a MP4
  5. Verificar archivo
  
Aserciones:
  ✓ Video generado
  ✓ Duración correcta (~4 seg a 30fps)
  ✓ Tamaño > 100KB
```

### **Escenario 4: Multi-idioma NLU**

```
E2E Test: test_multilanguage_execution

Pasos:
  1. Agent.set_language('en')
  2. Agent.execute("create a cube") → OK
  3. Agent.set_language('fr')
  4. Agent.execute("créer un cube") → OK
  5. Agent.set_language('de')
  6. Agent.execute("einen Würfel erstellen") → OK
  
Aserciones:
  ✓ Todos los idiomas funcionan
  ✓ Resultado idéntico en cada idioma
```

---

## **5. PRUEBAS DE SISTEMA COMPLETO**

### **5.1 Web UI + Agent + Blender**

```
Test: test_web_ui_full_integration

Precondiciones:
  - Flask server iniciado
  - Cliente WebSocket conectado
  - Blender disponible

Flujo:
  1. Frontend envía: "crear esfera"
  2. Backend Socket recibe
  3. Agent ejecuta
  4. SceneMonitor captura estado
  5. Socket emite: {status: 'success', render: 'url/...'}
  6. Frontend muestra render

Validaciones:
  ✓ Conexión WebSocket establecida
  ✓ Comando enrutado correctamente
  ✓ Respuesta enviada en tiempo < 5s
  ✓ Render disponible en URL
```

### **5.2 Asset Library + Web UI**

```
Test: test_asset_library_web_integration

Pasos:
  1. Frontend solicita lista de assets
  2. Backend retorna assets categorizados
  3. Usuario selecciona asset
  4. Asset se importa y aplica
  5. Render con asset importado

Validaciones:
  ✓ Lista carga sin errores
  ✓ Categorías correctas
  ✓ Asset se importa
  ✓ Render muestra asset
```

### **5.3 Vision Analyzer + Feedback Loop**

```
Test: test_vision_feedback_cycle

Pasos:
  1. Crear objeto
  2. Renderizar
  3. VisionAnalyzer analiza
  4. Detecta problemas (color, luz, etc.)
  5. Agent sugiere mejoras
  6. Aplicar mejora automática
  7. Renderizar nuevamente
  8. Comparar calidad

Validaciones:
  ✓ Análisis detecta cambios
  ✓ Mejoras aplicadas correctamente
  ✓ Calidad aumenta (score)
```

---

## **6. PRUEBAS DE EDGE CASES**

### **6.1 Errores de Entrada**

```
✓ test_empty_command
✓ test_malformed_json_parameters
✓ test_null_values
✓ test_unicode_characters
✓ test_extremely_long_input
```

### **6.2 Limites de Sistema**

```
✓ test_render_very_high_samples (1024+)
✓ test_massive_object_creation (100,000+ vertices)
✓ test_animation_very_long (10,000+ frames)
✓ test_concurrent_commands (5+ simultáneos)
```

### **6.3 Recuperación de Fallos**

```
✓ test_blender_crash_recovery
✓ test_corrupted_file_recovery
✓ test_network_interruption_websocket
✓ test_out_of_memory_handling
```

---

## **7. MATRIZ DE EJECUCIÓN**

### **Fase 1: Unitarias (Day 1 - Morning)**
```
Archivo: run_unit_tests.py
Comando: python -m pytest core/tests/ -v --cov=core
Esperado: 45+ tests, >85% coverage
Tiempo: ~15 min
```

### **Fase 2: Integración (Day 1 - Afternoon)**
```
Archivo: run_integration_tests.py
Comando: python -m pytest tests/integration/ -v
Esperado: 20+ tests verdes
Tiempo: ~20 min
```

### **Fase 3: E2E (Day 2 - Morning)**
```
Archivo: run_e2e_tests.py
Comando: python -m pytest tests/e2e/ -v
Precondición: Blender disponible
Esperado: 15+ tests verdes
Tiempo: ~45 min
```

### **Fase 4: Sistema (Day 2 - Afternoon)**
```
Archivo: run_system_tests.py
Comando: python -m pytest tests/system/ -v
Precondición: Web UI + Blender corriendo
Esperado: 10+ tests verdes
Tiempo: ~60 min
```

---

## **8. CRITERIOS DE ACEPTACIÓN**

### **PASS: Green Light ✅**
- [ ] 90+ tests ejecutados
- [ ] >85% tests exitosos
- [ ] Cobertura >80%
- [ ] Cero crashes en Blender
- [ ] Cero memory leaks detectados
- [ ] Tiempo promedio/comando < 5s
- [ ] Web UI responde < 3s

### **WARNINGS: Yellow Light ⚠️**
- Algunos tests flaky (intermitentes)
- Cobertura 70-85%
- Algunos edge cases fallando

### **FAIL: Red Light ❌**
- [ ] >10% tests fallando
- [ ] Crashes en Blender
- [ ] Memory leaks críticos
- [ ] Web UI no responde
- [ ] Comandos no ejecutan

---

## **9. HERRAMIENTAS Y CONFIGURACIÓN**

### **Testing Framework:**
```
pytest >= 7.0
pytest-cov (coverage)
pytest-xdist (parallelización)
unittest (base)
```

### **Blender Integration:**
```
bpy (Blender Python API)
blender --background --python test_script.py
```

### **Web Testing:**
```
pytest-asyncio (async tests)
python-socketio (WebSocket client)
requests (HTTP client)
```

### **Reportes:**
```
pytest-html (HTML reports)
coverage.py (coverage reports)
pytest-timeout (timeout detection)
```

---

## **10. ESTRUCTURA DE RESULTADOS**

```
reports/
├── unitarias/
│   ├── test_results_unitarias.html
│   ├── coverage.xml
│   └── summary.json
├── integracion/
│   ├── test_results_integracion.html
│   └── coverage.xml
├── e2e/
│   ├── test_results_e2e.html
│   ├── logs/
│   └── screenshots/
├── sistema/
│   ├── test_results_sistema.html
│   ├── performance.json
│   └── logs/
└── REPORTE_FINAL.md
```

---

## **11. PRÓXIMAS ACCIONES**

1. **Ejecutar Fase 1 (Unitarias)**
   - Tiempo: ~15 min
   - Objetivo: Validar componentes base

2. **Ejecutar Fase 2 (Integración)**
   - Tiempo: ~20 min
   - Objetivo: Validar interacción módulos

3. **Ejecutar Fase 3 (E2E)**
   - Tiempo: ~45 min
   - Precondición: Blender funcional
   - Objetivo: Flujos reales completos

4. **Ejecutar Fase 4 (Sistema)**
   - Tiempo: ~60 min
   - Precondición: Web UI + Blender
   - Objetivo: Validación total

5. **Generar Reporte Final**
   - Métricas: Cobertura, éxito rate, tiempos
   - Recomendaciones: Qué mejorar

---

**Estado:** Listo para iniciar pruebas  
**Siguiente paso:** Ejecutar Fase 1 (Tests Unitarias)
