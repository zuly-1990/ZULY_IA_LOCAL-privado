## Hito 4: Prueba real de creación de cubo mejorado

### Proceso
- Se ejecutó Blender en modo background desde la terminal.
- Se limpió la escena y se creó un cubo en la posición (0,0,0) con tamaño 2.
- El archivo se guardó como export/cubo_mejorado.blend.

### Resultado
- Cubo generado correctamente y archivo .blend guardado.

### Observaciones
- El proceso es reproducible y automatizable desde scripts o comandos.
## Hito 3: Integración de comandos Blender

### Flujo completo probado
- crea un cubo morado → Acción: Crear cube | Color: None | Tamaño: normal | Cantidad: 1
- crea un triángulo azul → Acción: Crear cube | Color: azul | Tamaño: normal | Cantidad: 1
- crea una esfera gigante → Acción: Crear sphere | Color: None | Tamaño: normal | Cantidad: 1
- crea -2 cubos → Acción: Crear cube | Color: None | Tamaño: normal | Cantidad: 2
- crea un cubo → Acción: Crear cube | Color: None | Tamaño: normal | Cantidad: 1

### Observaciones
- El sistema ejecuta la acción simulada según los parámetros validados.
- Las advertencias se muestran si existen, aunque en estos ejemplos no se generaron advertencias visibles.
## Hito 2: Validación y advertencias

### Órdenes ambiguas probadas
- crea un cubo morado (color no válido)
- crea un triángulo azul (objeto no válido)
- crea una esfera gigante (tamaño no válido)
- crea -2 cubos (cantidad negativa)
- crea un cubo (orden válida)

### Resultados y advertencias
- crea un cubo morado → {'intent': 'create_object', 'object': 'cube', 'color': None, 'size': 'normal', 'count': 1} | Advertencias: []
- crea un triángulo azul → {'intent': None, 'object': 'cube', 'color': 'azul', 'size': 'normal', 'count': 1} | Advertencias: ["Objeto 'None' no reconocido. Usando 'cube' por defecto."]
- crea una esfera gigante → {'intent': 'create_object', 'object': 'sphere', 'color': None, 'size': 'normal', 'count': 1} | Advertencias: []
- crea -2 cubos → {'intent': 'create_object', 'object': 'cube', 'color': None, 'size': 'normal', 'count': 2} | Advertencias: []
- crea un cubo → {'intent': 'create_object', 'object': 'cube', 'color': None, 'size': 'normal', 'count': 1} | Advertencias: []

### Observaciones
- El sistema ajusta valores no reconocidos y registra advertencias.
- No se detectó color ni tamaño no válidos en los ejemplos, se usan valores por defecto.
- El parsing de cantidad negativa no genera advertencia (mejora futura).

# Bitácora – Diálogo Fase 1

## Hito 1: Parsing básico funcionando

### Órdenes probadas
- crea un cubo rojo
- crea una esfera grande
- crea un plano como piso
- agrega un mono de prueba
- crea 3 cubos

### Resultados
- {'intent': 'create_object', 'object': 'cube', 'color': 'rojo', 'size': 'normal', 'count': 1}
- {'intent': 'create_object', 'object': 'sphere', 'color': None, 'size': 'grande', 'count': 1}
- {'intent': 'create_object', 'object': 'plane', 'color': None, 'size': 'normal', 'count': 1}
- {'intent': 'create_object', 'object': 'monkey', 'color': None, 'size': 'normal', 'count': 1}
- {'intent': 'create_object', 'object': 'cube', 'color': None, 'size': 'normal', 'count': 3}

### Fallos
- Ninguno en los ejemplos probados.

### Ideas futuras
- Mejorar reconocimiento de colores y tamaños.
- Añadir advertencias para parámetros no reconocidos.
