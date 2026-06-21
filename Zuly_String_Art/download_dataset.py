import os
import requests
import time

DATASET_DIR = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\Zuly_String_Art\Dataset"

if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)

print("Downloading 10 AI-generated portraits for analysis...")

for i in range(1, 11):
    filename = os.path.join(DATASET_DIR, f"portrait_{i}.jpg")
    try:
        # thispersondoesnotexist generates a new face on every GET request
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get("https://thispersondoesnotexist.com/", headers=headers, timeout=10)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download portrait {i}, status: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {i}: {e}")
    
    # Wait a bit so we don't get rate limited
    time.sleep(1.5)

print("Dataset download complete.")
