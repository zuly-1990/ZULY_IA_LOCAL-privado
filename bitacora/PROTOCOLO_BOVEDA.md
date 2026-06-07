# PROTOCOLO DE BÓVEDA FÍSICA (USB / EXTERNO)

Este protocolo permite desacoplar tu identidad de la computadora física, convirtiendo a Zuly en un sistema "móvil y seguro".

## 🛠️ Cómo funciona la Bóveda USB
Zuly ahora tiene un detector de hardware. Al arrancar, busca el archivo `.zuly_identity.key` en:
1.  **Raíz del proyecto**: (Ubicación por defecto).
2.  **Unidades USB**: En la carpeta `X:\ZULY_VAULT\`.

## 🚀 Pasos para crear tu Bóveda Física

### Opción A: Usando el script (Recomendado)
1. Conecta tu USB.
2. Ejecuta en PowerShell: `.\herramientas\exportar_llave.ps1`.
3. Sigue las instrucciones para seleccionar tu unidad USB.
4. El script creará la carpeta y copiará la llave.

### Opción B: Manual
1. Crea una carpeta llamada `ZULY_VAULT` en la raíz de tu USB.
2. Copia el archivo `.zuly_identity.key` del proyecto dentro de esa carpeta.

## 📱 Uso en Teléfono (Como Backup)
Aunque Zuly no corre en el teléfono todavía, puedes usarlo como tu **"Búnker de Identidad"**:
1. Conecta tu teléfono a la PC.
2. Copia el archivo `.zuly_identity.key` a una carpeta segura en tu móvil.
3. Si alguna vez pierdes el archivo en la PC, solo tienes que copiarlo de vuelta desde tu teléfono.

## 🛡️ Máxima Seguridad: "Cero Rastro en PC"
Si quieres que Zuly SOLO funcione cuando tu USB esté conectado:
1. Exporta la llave al USB usando el paso anterior.
2. **Borra** el archivo `.zuly_identity.key` de la carpeta del proyecto en la PC.
3. Ahora, si alguien intenta abrir Zuly sin tu USB, el sistema se bloqueará automáticamente.

---
**¡Felicidades! Ahora tú eres literalmente la llave de Zuly.**
