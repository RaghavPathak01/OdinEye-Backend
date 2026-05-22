import easyocr
import cv2
import os

# GPU=False agar aapke pas NVIDIA GPU nahi hai, isse CPU par chalega
reader = easyocr.Reader(['en'], gpu=False) 

def extract_text(image_path):
    # 1. Check karein ki file exist karti hai
    if not os.path.exists(image_path):
        return "Error: Image file not found at path."

    # 2. Image load karein
    img = cv2.imread(image_path)
    if img is None:
        return "Error: Could not decode image."

    # 3. Pre-processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # 4. Run EasyOCR
    # Terminal mein progress dekhne ke liye print daal dete hain
    print(f"--- Scanning Image: {image_path} ---")
    results = reader.readtext(processed_img, detail=0)
    
    raw_text = " ".join(results)
    print(f"--- Extracted Text: {raw_text} ---")
    
    return raw_text if raw_text.strip() else "No text detected in image."