# Estructura Generada del Núcleo de Zuly - Fase 1

Este documento resume la estructura de archivos y módulos generada para la Fase 1 del núcleo de Zuly, siguiendo la hoja de ruta técnica proporcionada.

## Módulos Base del Núcleo (`core/`)

-   **`core/agent.py`**:
    -   **Intención**: Define el `Agent` principal de Zuly. Actúa como el orquestador de comandos, cargador de módulos y responsable de diagnósticos iniciales.
    -   **Dependencias**: `core.commands.base_command`, `core.diagnostics.diagnostics`, `core.utils.helpers`.

-   **`core/utils/helpers.py`**:
    -   **Intención**: Contiene funciones de utilidad compartidas, como `log_message` y `format_name`, para evitar dependencias circulares y promover la modularidad entre otros módulos del núcleo.
    -   **Dependencias**: Ninguna dependencia directa a `agent.py`.

## Módulos de Comandos (`core/commands/`)

-   **`core/commands/__init__.py`**:
    -   **Intención**: Archivo de inicialización del módulo de comandos.

-   **`core/commands/base_command.py`**:
    -   **Intención**: Define la clase abstracta `BaseCommand`. Sirve como interfaz para todos los comandos ejecutables en Zuly, asegurando una estructura uniforme con métodos como `ejecutar()`, `validar()` y `descripcion()`.

-   **`core/commands/blender_commands.py`**:
    -   **Intención**: Contiene comandos específicos para interactuar con Blender, como `CrearPrimitiva`, `MoverObjeto` y `ExportarLog`. Heredan de `BaseCommand`.

-   **`core/commands/system_commands.py`**:
    -   **Intención**: Define comandos para operaciones a nivel del sistema, como `ReiniciarSistema` y `DiagnosticoSistema`. Heredan de `BaseCommand`.

## Módulos de Diagnóstico (`core/diagnostics/`)

-   **`core/diagnostics/__init__.py`**:
    -   **Intención**: Archivo de inicialización del módulo de diagnóstico.

-   **`core/diagnostics/diagnostics.py`**:
    -   **Intención**: Provee funcionalidades para realizar diagnósticos del sistema Zuly, incluyendo `revisar_estado()`, `revisar_modulos()` y `dependencia_ok()`.
    -   **Dependencias**: `core.utils.helpers` (no depende de `agent.py`).

-   **`core/diagnostics/log_manager.py`**:
    -   **Intención**: Gestiona las operaciones de logging del proyecto Zuly, permitiendo `escribir()`, `leer()` y `exportar()` registros.

-   **`core/diagnostics/system_check.py`**:
    -   **Intención**: Realiza verificaciones del entorno del sistema para asegurar la compatibilidad y el correcto funcionamiento, como `verificar_entorno()`, `version_python()` y `version_blender()`.

## Módulos de Estabilidad (`core/stability/`)

-   **`core/stability/__init__.py`**:
    -   **Intención**: Archivo de inicialización del módulo de estabilidad.

-   **`core/stability/safe_guard.py`**:
    -   **Intención**: Proporciona mecanismos de salvaguarda y aislamiento para operaciones críticas, con métodos como `proteger()`, `aislamiento()` y `validar_integridad()`.

-   **`core/stability/fail_recovery.py`**:
    -   **Intención**: Implementa mecanismos de recuperación ante fallos, incluyendo `recuperar()`, `reiniciar_proceso()` y `registro_fallo()`.

## Pruebas Iniciales (`core/tests/`)

-   **`core/tests/__init__.py`**:
    -   **Intención**: Archivo de inicialización del módulo de pruebas.

-   **`core/tests/test_crear_primitiva.py`**:
    -   **Intención**: Contiene pruebas unitarias para el comando `CrearPrimitiva`, con la función `test_crear_cubo()`.
    -   **Dependencias**: `core.commands.blender_commands`.

-   **`core/tests/test_local.py`**:
    -   **Intención**: Incluye pruebas locales básicas para verificar la importación y ejecución mínima de componentes clave de Zuly.
    -   **Dependencias**: `core.agent`, `core.commands.blender_commands`, `core.diagnostics.diagnostics`, `core.utils.helpers`.

## Archivos en la Raíz del Proyecto

-   **`controlar_blender.py`**:
    -   **Intención**: Módulo para controlar la ejecución de Blender y la interacción con sus scripts. Contiene funciones `abrir_blender()`, `ejecutar_script()` y la clase `BlenderController`.

## Scripts Externos (`herramientas/scripts_externos/`)

-   **`herramientas/scripts_externos/run_crear_primitiva.py`**:
    -   **Intención**: Script externo para invocar directamente el comando `CrearPrimitiva` de Zuly.
    -   **Dependencias**: `core.commands.blender_commands`, `core.agent`.

-   **`herramientas/scripts_externos/test_local.ps1`**:
    -   **Intención**: Script de PowerShell para ejecutar pruebas locales o comandos de diagnóstico, interactuando con Zuly.











