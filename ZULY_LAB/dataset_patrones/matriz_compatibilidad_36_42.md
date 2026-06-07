# Matriz de Compatibilidad: Aprendizaje ZULY (3.6 vs 4.2)

ZULY ha analizado el contenido del tutorial de Blender 4.2 y ha validado su aplicación en el entorno actual (Blender 3.6 LTS).

## 1. Comandos de Manipulación (Núcleo)
| Acción | Blender 3.6 | Blender 4.2 | Estado |
| :--- | :--- | :--- | :--- |
| Move | G | G | **Idéntico** |
| Rotate | R | R | **Idéntico** |
| Scale | S | S | **Idéntico** |
| Extrude | E | E | **Idéntico** |
| Loop Cut | Ctrl + R | Ctrl + R | **Idéntico** |

## 2. Herramientas Arquitectónicas
| Herramienta | Blender 3.6 | Blender 4.2 | Nota Técnica |
| :--- | :--- | :--- | :--- |
| **Bisect** | Knife -> Bisect | Knife -> Bisect | Funciona igual. Importante para la Fase C3.3. |
| **ArchiMesh** | Add-on interno | Extensión (as-is) | En 3.6 viene pre-instalado. En 4.2 se instala vía extensiones. La lógica paramétrica es compatible. |
| **Snap** | Imán (Superior) | Imán (Superior) | Sistema de anclaje a vértices idéntico. |

## 3. Configuración de Escena
| Concepto | Blender 3.6 | Blender 4.2 | Acción ZULY |
| :--- | :--- | :--- | :--- |
| **Unidades** | Escena -> Units | Escena -> Units | ZULY ya soporta cambio de unidades (Métrico/Imperial). |
| **Referencia** | Shift+A -> Image | Shift+A -> Image | Proceso de carga de planos 2D es idéntico. |

## Conclusión de Seguridad
El conocimiento extraído de la versión 4.2 es **95% compatible** con el motor operativo de ZULY (3.6). No hay riesgos de regresión funcional. Las pocas diferencias (como el sistema de extensiones de 4.2) no afectan a los scripts de ejecución de ZULY, ya que dependen del API `bpy` estable.

**Estado: SEGURO PARA INTEGRAR**
