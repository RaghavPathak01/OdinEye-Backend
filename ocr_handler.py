import easyocr
import cv2
import os

reader = easyocr.Reader(['en'], gpu=False) 

def extract_text(image_path):
    if not os.path.exists(image_path):
        return "Error: Image file not found at path."

    img = cv2.imread(image_path)
    if img is None:
        return "Error: Could not decode image."

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    print(f"--- Scanning Image: {image_path} ---")
    results = reader.readtext(processed_img, detail=0)
    
    raw_text = " ".join(results)
    print(f"--- Extracted Text: {raw_text} ---")
    
    return raw_text if raw_text.strip() else "No text detected in image."