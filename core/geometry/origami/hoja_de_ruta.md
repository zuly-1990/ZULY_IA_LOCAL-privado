# 🗺️ Hoja de Ruta: Proyecto Zuly Origami

Esta es la ruta de aprendizaje y desarrollo que seguirá Zuly para dominar el diseño paramétrico de muebles transformables y arquitectura desplegable. Lo abordaremos de forma progresiva, de menor a mayor complejidad matemática.

---

## FASE 1: Fundamentos Geométricos (El Primer Doblez)
Antes de construir una silla transformable, Zuly debe entender la matemática de una bisagra.
*   **Hito 1:** Escribir un script en Python para Blender que tome un plano 2D, haga un corte perfecto en el centro, y rote una mitad exactamente a 90 grados sin romper la malla.
*   **Hito 2:** Programar un algoritmo de detección de colisiones. Zuly debe calcular el grosor del material (ej. madera de 15mm) para que al doblarse a 180 grados, la madera no se traspase a sí misma.
*   **Meta de la fase:** Crear una caja o un asiento súper básico plegable desde un solo plano de madera.

---

## FASE 2: Cinemática Inversa y Rigging (El Movimiento)
Aquí abordamos el **Punto 1 y 4** de nuestro análisis (Animación interactiva de Muebles).
*   **Hito 1:** Programar a Zuly para que inyecte un "Esqueleto Virtual" (Armature/Bones) dentro del mueble de Blender usando Python.
*   **Hito 2:** Configurar *Shape Keys* o restricciones de cinemática inversa. Esto significa que Zuly programará el mueble para que, si el usuario tira de la mesa hacia arriba, las patas de la silla se doblen automáticamente siguiendo reglas físicas estrictas.
*   **Meta de la fase:** Un archivo `.blend` de una silla que se hace mesa, que el cliente pueda abrir, mover un deslizador de 0 a 100%, y ver la transformación animada perfectamente.

---

## FASE 3: Algoritmo de "Desdoblamiento" (Corte Láser y CNC)
Aquí abordamos el **Punto 2** (Del 3D a la vida real). Es el reto de ingeniería más grande.
*   **Hito 1:** Crear un algoritmo matemático que tome el mueble final (ya con grosor y volumen) y aplique "Unrolling" (desenrollado). 
*   **Hito 2:** El script debe mapear cada pieza 3D y acomodarla de forma plana en un lienzo 2D (Nesting) para aprovechar al máximo la plancha de madera y no desperdiciar material.
*   **Hito 3:** Exportación automatizada a formato `.DXF` o `.SVG` listo para la máquina CNC.
*   **Meta de la fase:** ¡Fabricar el primer prototipo de cartón o madera en la vida real usando los planos generados por Zuly!

---

## FASE 4: Arquitectura Desplegable a Gran Escala
Aquí abordamos el **Punto 3** (Tiny Houses y Refugios).
*   **Hito 1:** Escalar las matemáticas. En lugar de madera de 15mm, Zuly calculará paneles estructurales con bisagras industriales.
*   **Hito 2:** Conectar este módulo con su cerebro "Arquitecto" (DeepSeek). Tú le dirás a DeepSeek: *"Diseña un refugio de 5x5 metros que quepa en un camión"*, y DeepSeek generará el código que usa la lógica de Origami para plegar la casa en un cubo de 2x2 metros.
*   **Meta de la fase:** El primer plano arquitectónico desplegable 100% generado por Inteligencia Artificial.
