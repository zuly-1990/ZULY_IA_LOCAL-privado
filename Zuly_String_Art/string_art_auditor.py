import numpy as np
from PIL import Image
import sys
import math

def calculate_mse(imageA, imageB):
    # Sum of squared differences
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def main():
    if len(sys.argv) < 3:
        print("Usage: python string_art_auditor.py <original_image> <generated_image>")
        return

    original_path = sys.argv[1]
    generated_path = sys.argv[2]

    imgA = Image.open(original_path).convert('L')
    imgB = Image.open(generated_path).convert('L')

    # Resize imgA to match imgB just in case
    if imgA.size != imgB.size:
        imgA = imgA.resize(imgB.size)

    # Convert to numpy arrays
    np_A = np.array(imgA)
    np_B = np.array(imgB)

    # Apply circular mask so we only compare inside the circle
    h, w = np_A.shape
    center = (w//2, h//2)
    radius = w//2 - 2
    y, x = np.ogrid[:h, :w]
    mask = (x - center[0])**2 + (y - center[1])**2 <= radius**2

    # Set outside to white for both
    np_A[~mask] = 255
    np_B[~mask] = 255

    mse = calculate_mse(np_A, np_B)
    
    # Calculate a score out of 100
    # Max possible MSE for 8-bit images is 255^2 = 65025
    # Let's map it: 0 MSE = 100%, 65025 MSE = 0%
    score = max(0, 100 - (mse / 65025) * 100)
    
    print(f"MSE: {mse:.2f}")
    print(f"Auditor_Score: {score:.2f}%")

if __name__ == "__main__":
    main()
