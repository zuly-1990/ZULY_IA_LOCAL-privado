import numpy as np
from PIL import Image, ImageDraw, ImageEnhance
import json
import math
import sys

IMAGE_PATH = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Admin\.gemini\antigravity\brain\c39cd392-d7db-4d2c-875e-6664c3cb2a95\portrait_for_string_art_1782063089154.png"
NUM_PINS = int(sys.argv[2]) if len(sys.argv) > 2 else 250
MAX_LINES = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
OUTPUT_PREFIX = sys.argv[4] if len(sys.argv) > 4 else "result"

OUTPUT_JSON = f"pin_sequence_{OUTPUT_PREFIX}.json"
OUTPUT_IMAGE = f"string_art_{OUTPUT_PREFIX}.png"

LINE_WEIGHT = 20
RESOLUTION = 800
MIN_DISTANCE = NUM_PINS // 10  # REGLA DE VRELLIS: Prohibido hilos cortos

def get_line_pixels(x0, y0, x1, y1):
    pixels = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x1:
            pixels.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            pixels.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    pixels.append((x, y))
    return pixels

def precalculate_lines(pins):
    print("Precalculating lines...")
    lines = {}
    for i in range(NUM_PINS):
        for j in range(i + 1, NUM_PINS):
            x0, y0 = pins[i]
            x1, y1 = pins[j]
            pixels = get_line_pixels(int(x0), int(y0), int(x1), int(y1))
            lines[(i, j)] = pixels
            lines[(j, i)] = pixels
    return lines

def main():
    print("Loading image...")
    img = Image.open(IMAGE_PATH).convert('L')
    
    # REGLA DE VRELLIS: Mejorar contraste al máximo para que los hilos no duden
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)  # Aumentamos contraste al 150%
    
    # Resize and crop to square
    w, h = img.size
    min_dim = min(h, w)
    start_x = w//2 - min_dim//2
    start_y = h//2 - min_dim//2
    img = img.crop((start_x, start_y, start_x+min_dim, start_y+min_dim))
    img = img.resize((RESOLUTION, RESOLUTION))

    img_array = np.array(img, dtype=np.float32)
    img_array = 255.0 - img_array # Invert (Zonas oscuras ahora son altas = 255)

    # Apply circular mask
    center = (RESOLUTION//2, RESOLUTION//2)
    radius = RESOLUTION//2 - 2
    for y in range(RESOLUTION):
        for x in range(RESOLUTION):
            if (x - center[0])**2 + (y - center[1])**2 > radius**2:
                img_array[y, x] = 0

    print("Generating pins...")
    pins = []
    for i in range(NUM_PINS):
        angle = 2 * math.pi * i / NUM_PINS
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        pins.append((x, y))

    lines = precalculate_lines(pins)
    sequence = [0]
    current_pin = 0
    error_img = img_array.copy()

    # Create white image for drawing result
    result_img = Image.new('L', (RESOLUTION, RESOLUTION), 255)
    draw = ImageDraw.Draw(result_img)

    print("Starting greedy algorithm...")
    for step in range(MAX_LINES):
        if step % 500 == 0:
            print(f"Step {step}/{MAX_LINES}")

        best_score = -1
        best_pin = -1

        for next_pin in range(NUM_PINS):
            if next_pin == current_pin: continue
            
            # REGLA DE VRELLIS: Prohibido saltar a clavos demasiado cercanos
            dist_clockwise = abs(next_pin - current_pin)
            dist_counter = NUM_PINS - dist_clockwise
            if min(dist_clockwise, dist_counter) < MIN_DISTANCE:
                continue

            pixels = lines[(current_pin, next_pin)]
            score = 0
            for px, py in pixels:
                if 0 <= px < RESOLUTION and 0 <= py < RESOLUTION:
                    score += error_img[py, px]
            
            # Penalizamos levemente hilos muy cortos incluso si pasaron el filtro de min_distance
            score = score / max(len(pixels), 1)

            if score > best_score:
                best_score = score
                best_pin = next_pin

        if best_pin == -1:
            break

        pixels = lines[(current_pin, best_pin)]
        for px, py in pixels:
            if 0 <= px < RESOLUTION and 0 <= py < RESOLUTION:
                # Restamos oscuridad de la imagen original
                error_img[py, px] = max(0, error_img[py, px] - LINE_WEIGHT)

        # Draw line on result
        draw.line([pins[current_pin], pins[best_pin]], fill=0, width=1)

        sequence.append(best_pin)
        current_pin = best_pin

    print("Algorithm complete. Saving output...")
    with open(OUTPUT_JSON, "w") as f:
        json.dump(sequence, f)

    result_img.save(OUTPUT_IMAGE)
    print("Done! Sequence length:", len(sequence))

if __name__ == "__main__":
    main()
