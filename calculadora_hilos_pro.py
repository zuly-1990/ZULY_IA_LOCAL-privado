import numpy as np
import cv2
import json
import math
import random
import time

def generate_string_art_pro(imagen_entrada, num_clavos=288, num_iteraciones=3500, radio_escala=0.95):
    print("Iniciando motor PRO (Matriz Pre-calculada)...")
    t0 = time.time()
    
    # Cargar y preparar imagen
    img = cv2.imread(imagen_entrada, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("No se pudo cargar la imagen.")
    
    # Redimensionar a 500x500 para que el cálculo matemático sea instantáneo
    img = cv2.resize(img, (500, 500))
    
    img_gris = img.astype(np.float32)
    alto, ancho = img_gris.shape
    lienzo = np.ones((alto, ancho), dtype=np.float32) * 255.0
    
    # Calcular coordenadas de los clavos
    centro_x, centro_y = ancho / 2.0, alto / 2.0
    radio = min(ancho, alto) / 2.0 * radio_escala
    
    clavos_x = np.zeros(num_clavos, dtype=np.int32)
    clavos_y = np.zeros(num_clavos, dtype=np.int32)
    
    for i in range(num_clavos):
        angulo = 2.0 * math.pi * i / num_clavos - math.pi / 2.0
        clavos_x[i] = max(0, min(ancho - 1, int(centro_x + radio * math.cos(angulo))))
        clavos_y[i] = max(0, min(alto - 1, int(centro_y + radio * math.sin(angulo))))
        
    print(f"[{time.time()-t0:.2f}s] Pre-calculando 41,472 trayectorias posibles...")
    
    # PRE-CALCULAR TODAS LAS LÍNEAS (La magia de la velocidad)
    # Diccionario 2D: trayectorias[A][B] = (array_x, array_y) de los pixeles que conforman esa línea
    trayectorias = {}
    for i in range(num_clavos):
        trayectorias[i] = {}
        for j in range(num_clavos):
            if i == j: continue
            
            # Usar cv2.line en una máscara temporal para extraer los pixeles de esta línea una sola vez
            mask = np.zeros((alto, ancho), dtype=np.uint8)
            cv2.line(mask, (clavos_x[i], clavos_y[i]), (clavos_x[j], clavos_y[j]), 255, 1)
            # np.where devuelve (y_indices, x_indices)
            y_idx, x_idx = np.where(mask == 255)
            trayectorias[i][j] = (y_idx, x_idx)

    print(f"[{time.time()-t0:.2f}s] Trayectorias en memoria. Calculando {num_iteraciones} hilos...")
    
    secuencia_clavos = []
    clavo_actual = 0
    secuencia_clavos.append(clavo_actual)
    
    distancia_min = num_clavos // 15
    
    # Bucle principal hiper-rápido
    for iteracion in range(num_iteraciones):
        mejor_puntuacion = -1.0
        mejor_destino = -1
        
        # Oscuridad actual de la imagen (donde 0 es blanco y 255 es negro profundo)
        oscuridad_img = 255.0 - img_gris
        
        for destino in range(num_clavos):
            # Filtro de distancia mínima
            diff = abs(destino - clavo_actual)
            if destino == clavo_actual or diff < distancia_min or diff > num_clavos - distancia_min:
                continue
            
            # Recuperar coordenadas de la trayectoria pre-calculada
            y_idx, x_idx = trayectorias[clavo_actual][destino]
            
            if len(y_idx) > 0:
                # Sumar oscuridad de todos los píxeles de la línea
                puntuacion = np.sum(oscuridad_img[y_idx, x_idx])
                # Dividir por la longitud de la línea para evitar sesgo hacia líneas largas
                puntuacion /= len(y_idx)
            else:
                puntuacion = 0.0
                
            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_destino = destino
                
        if mejor_destino != -1 and mejor_puntuacion > 0:
            y_idx, x_idx = trayectorias[clavo_actual][mejor_destino]
            
            # Aclarar la imagen donde pasó el hilo para no volver a pasar
            # (Si restamos oscuridad_img, es sumar a img_gris)
            img_gris[y_idx, x_idx] = np.clip(img_gris[y_idx, x_idx] + 25.0, 0, 255)
            
            # Dibujar en el lienzo final
            x1, y1 = clavos_x[clavo_actual], clavos_y[clavo_actual]
            x2, y2 = clavos_x[mejor_destino], clavos_y[mejor_destino]
            cv2.line(lienzo, (x1, y1), (x2, y2), 0.0, 1, cv2.LINE_AA)
            
            clavo_actual = mejor_destino
            secuencia_clavos.append(clavo_actual)
        else:
            clavo_actual = random.randint(0, num_clavos - 1)
            secuencia_clavos.append(clavo_actual)
            
        if (iteracion + 1) % 500 == 0:
            print(f"  -> Hilos: {iteracion + 1}/{num_iteraciones}")

    print(f"[{time.time()-t0:.2f}s] Cálculo finalizado. Guardando JSON y PNG...")
    
    with open('secuencia_clavos.json', 'w') as f:
        json.dump(secuencia_clavos, f)
        
    cv2.imwrite('string_art_resultado.png', lienzo.astype(np.uint8))
    print(f"[{time.time()-t0:.2f}s] ¡Todo listo!")

if __name__ == "__main__":
    import os
    imagen = r"C:\Users\Admin\.gemini\antigravity\brain\c39cd392-d7db-4d2c-875e-6664c3cb2a95\house_wireframe_1782614502948.png"
    if not os.path.exists(imagen):
        print("Asegúrate de que la ruta a la imagen sea correcta.")
    else:
        generate_string_art_pro(imagen, num_clavos=288, num_iteraciones=3500)
