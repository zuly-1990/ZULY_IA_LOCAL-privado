# IDENTIDAD Y PROTECCIÓN DE DECISIONES - PROTOCOLO DE AUTORÍA

**Módulo de Seguridad:** `core/security/identity.py`  
**Archivo de Llave:** `.zuly_identity.key` (Oculto)

## 🛡️ Propósito
Garantizar que solo el autor verificado en la máquina local pueda autorizar el aprendizaje o la ejecución de comandos críticos, protegiendo a Zuly de manipulaciones externas o ejecuciones accidentales con baja confianza.

## 🔐 Mecanismo de Identidad Local

### 1. Generación de Llave
- Al iniciar Zuly por primera vez, el sistema genera automáticamente un **UUID4 único**.
- Este UUID se guarda en `.zuly_identity.key` en el directorio raíz.
- En sistemas Windows, el archivo se marca automáticamente como **Oculto**.

### 2. Verificación de Autoría
- Zuly comprueba la existencia y validez de la llave local en cada arranque y antes de procesar cualquier intención.
- Si la llave no está presente o no es legible, el sistema entra en **Modo de Seguridad Estricto**, bloqueando cualquier acción que implique aprendizaje o cambios en la escena.

## 🌀 Estados que Requieren Autoría

| Estado | Requiere Autoría | Condición de Confianza |
| :--- | :--- | :--- |
| **Observación** | No | N/A |
| **Evaluación** | No | N/A |
| **Ejecución Técnica** | SÍ | > 90% |
| **Aprendizaje Supervisado** | SÍ | 100% (Manual) |
| **Bloqueo Ético** | Auto | < 90% o No Autorizado |

## 🚦 Reglas de Transición Seguras

1.  **De Evaluación a Ejecución**: Solo si el autor está verificado Y la confianza de la interpretación es `>= 90%`.
2.  **Registro de Decisiones**: Solo ocurre cuando el usuario confirma explícitamente y el sistema detecta que el autor es genuino.
3.  **Transición a Bloqueo**: Se activa de inmediato si se detecta un fallo en la lectura de la llave o si los parámetros de la orden son ambiguos.

## 🚫 Protocolos de Rechazo

- **Rechazo por Identidad**: "Bloqueo Ético: Autor no verificado. Solo se permite el modo de observación."
- **Rechazo por Incertidumbre**: "Petición con ambigüedad excedida. Se requiere reformulación clara para evitar acciones no deseadas."

---
> [!IMPORTANT]
> Nunca compartas ni subas el archivo `.zuly_identity.key`. Es tu ancla de autoridad personal sobre el sistema.
