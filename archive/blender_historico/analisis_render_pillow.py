
"""
Script de análisis de imagen renderizada usando Pillow.
Calcula brillo promedio, contraste y guarda una miniatura.
"""

from PIL import Image
import os
import statistics

# Ruta de la imagen renderizada (ajusta si usas otra)
img_path = os.path.join('export', 'pruebas_cubo', 'frames_animacion_tres_cubos_sin_color', 'tres_cubos_sin_color_frontal.png')

# Verifica que la imagen exista
if not os.path.exists(img_path):
    print(f"No se encontró la imagen: {img_path}")
    exit(1)

# Abrir imagen y convertir a escala de grises
img = Image.open(img_path).convert('L')

# Calcular brillo promedio
pixels = list(img.getdata())
brillo_promedio = sum(pixels) / len(pixels)
print(f"Brillo promedio de la imagen: {brillo_promedio:.2f} (0=negro, 255=blanco)")

# Calcular contraste (desviación estándar)
contraste = statistics.stdev(pixels)
print(f"Contraste de la imagen: {contraste:.2f}")

# Mostrar dimensiones
print(f"Dimensiones de la imagen: {img.width}x{img.height}")

# Guardar una versión miniatura de la imagen
img.thumbnail((128, 128))
miniatura_path = os.path.join('export', 'pruebas_cubo', 'frames_animacion_tres_cubos_sin_color', 'miniatura.png')
img.save(miniatura_path)
print(f"Miniatura guardada en: {miniatura_path}")
