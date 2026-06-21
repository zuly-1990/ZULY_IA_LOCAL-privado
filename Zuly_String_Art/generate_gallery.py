import os
import subprocess

DATASET_DIR = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\Zuly_String_Art\Dataset"
RESULTS_DIR = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\Zuly_String_Art\Resultados_Galeria"
HTML_FILE = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\Zuly_String_Art\analisis_galeria.html"

if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

# Generate HTML header
html_content = """
<html>
<head>
    <title>Laboratorio de Hilos: Análisis de 10 Rostros</title>
    <style>
        body { font-family: sans-serif; background-color: #1a1a1a; color: white; text-align: center; }
        .gallery { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; padding: 20px; }
        .item { background: #2a2a2a; border-radius: 10px; padding: 15px; width: 400px; box-shadow: 0 4px 8px rgba(0,0,0,0.5); }
        .images { display: flex; justify-content: space-between; }
        img { width: 180px; height: 180px; border-radius: 5px; object-fit: cover; }
        h3 { margin-top: 0; color: #ffeb3b; }
        .label { font-size: 0.8em; color: #aaa; margin-top: 5px; }
    </style>
</head>
<body>
    <h1>Laboratorio de Análisis de Hilos (String Art Vrellis)</h1>
    <p>Comparativa visual de 10 rostros procesados con el algoritmo de Petros Vrellis (1000 hilos).</p>
    <div class="gallery">
"""

for i in range(1, 11):
    original_img = os.path.join(DATASET_DIR, f"portrait_{i}.jpg")
    output_prefix = f"rostro_{i}"
    result_img = os.path.join(RESULTS_DIR, f"string_art_{output_prefix}.png")
    
    if os.path.exists(original_img):
        print(f"Procesando rostro {i} / 10...")
        # Run string art algorithm: 300 pins, 1000 lines (fast analysis)
        subprocess.run(["python", "string_art_algorithm.py", original_img, "300", "1000", output_prefix], cwd=r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\Zuly_String_Art")
        
        # Move the output images to RESULTS_DIR
        local_result = f"string_art_{output_prefix}.png"
        if os.path.exists(local_result):
            os.rename(local_result, result_img)
            
            # Delete the JSON to save space since we only care about images
            if os.path.exists(f"pin_sequence_{output_prefix}.json"):
                os.remove(f"pin_sequence_{output_prefix}.json")

        # Add to HTML
        html_content += f"""
        <div class="item">
            <h3>Prueba #{i}</h3>
            <div class="images">
                <div>
                    <img src="file:///{original_img.replace(chr(92), '/')}" />
                    <div class="label">Foto Original</div>
                </div>
                <div>
                    <img src="file:///{result_img.replace(chr(92), '/')}" />
                    <div class="label">Resultado Hilos</div>
                </div>
            </div>
        </div>
        """

html_content += """
    </div>
</body>
</html>
"""

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Galería generada en: {HTML_FILE}")
