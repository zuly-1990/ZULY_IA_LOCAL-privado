import numpy as np
import cv2
import json
import math
import random

def string_art_cv2(imagen_entrada, num_clavos=288, num_iteraciones=3500, radio_escala=0.95):
    # Cargar imagen en escala de grises
    img = cv2.imread(imagen_entrada, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("No se pudo cargar la imagen.")
    
    # Invertir para que lo oscuro sea blanco (más fácil de restar)
    # img_calc = 255 - img
    # Trabajaremos restando 255 a la imagen gris original
    img_gris = img.astype(np.float32)
    alto, ancho = img_gris.shape
    lienzo = np.ones((alto, ancho), dtype=np.float32) * 255.0
    
    centro_x = ancho / 2.0
    centro_y = alto / 2.0
    radio = min(ancho, alto) / 2.0 * radio_escala
    
    clavos_x = np.zeros(num_clavos, dtype=np.int32)
    clavos_y = np.zeros(num_clavos, dtype=np.int32)
    
    for i in range(num_clavos):
        angulo = 2.0 * math.pi * i / num_clavos - math.pi / 2.0
        x = int(centro_x + radio * math.cos(angulo))
        y = int(centro_y + radio * math.sin(angulo))
        clavos_x[i] = max(0, min(ancho - 1, x))
        clavos_y[i] = max(0, min(alto - 1, y))
    
    secuencia_clavos = []
    clavo_actual = random.randint(0, num_clavos - 1)
    secuencia_clavos.append(clavo_actual)
    
    print(f"Iniciando generación con OpenCV C++ ({num_iteraciones} líneas)...")
    
    # Crear una máscara temporal para el muestreo de líneas
    mask = np.zeros((alto, ancho), dtype=np.uint8)
    
    for iteracion in range(num_iteraciones):
        if (iteracion + 1) % 500 == 0:
            print(f"  Progreso: {iteracion + 1}/{num_iteraciones} hilos calculados")
        
        mejor_puntuacion = -1.0
        mejor_destino = -1
        
        x1, y1 = clavos_x[clavo_actual], clavos_y[clavo_actual]
        
        for destino in range(num_clavos):
            if destino == clavo_actual: continue
            
            distancia_min = num_clavos // 15
            diff = abs(destino - clavo_actual)
            if diff < distancia_min or diff > num_clavos - distancia_min:
                continue
            
            x2, y2 = clavos_x[destino], clavos_y[destino]
            
            # Dibujar línea blanca de 1 pixel sobre máscara negra
            mask.fill(0)
            cv2.line(mask, (x1, y1), (x2, y2), 255, 1)
            
            # La puntuación es la media de oscuridad calculada 100% en C++ usando mask
            oscuridad = 255.0 - img_gris
            # cv2.mean devuelve una tupla (val, 0, 0, 0), tomamos el primer valor
            puntuacion = cv2.mean(oscuridad, mask=mask)[0]
            
            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_destino = destino
        
        if mejor_destino != -1 and mejor_puntuacion > 0:
            x_dest, y_dest = clavos_x[mejor_destino], clavos_y[mejor_destino]
            
            # Aclarar imagen (simular que ya pasamos hilo por ahí)
            mask.fill(0)
            cv2.line(mask, (x1, y1), (x_dest, y_dest), 255, 1)
            
            # Sumar 25 a los pixeles donde pasamos (hacerlos más blancos)
            # cv2.add() con máscara es miles de veces más rápido en C++ que numpy
            cv2.add(img_gris, 25.0, dst=img_gris, mask=mask)
            # Asegurar que no pase de 255
            np.clip(img_gris, 0, 255, out=img_gris)
            
            # Dibujar hilo en el lienzo final
            cv2.line(lienzo, (x1, y1), (x_dest, y_dest), 0.0, 1, cv2.LINE_AA)
            
            clavo_actual = mejor_destino
            secuencia_clavos.append(clavo_actual)
        else:
            clavo_actual = random.randint(0, num_clavos - 1)
            secuencia_clavos.append(clavo_actual)
    
    with open('secuencia_clavos.json', 'w') as f:
        json.dump([int(x) for x in secuencia_clavos], f)
    
    cv2.imwrite('string_art_resultado.png', lienzo.astype(np.uint8))
    
    print("¡Terminado en tiempo récord!")
    return secuencia_clavos

if __name__ == "__main__":
    imagen_real = r"C:\Users\Admin\.gemini\antigravity\brain\c39cd392-d7db-4d2c-875e-6664c3cb2a95\portrait_for_string_art_1782063089154.png"
    string_art_cv2(imagen_real, num_clavos=288, num_iteraciones=3500)