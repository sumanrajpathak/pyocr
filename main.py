from fastapi import FastAPI, File, UploadFile
# from PIL import Image, ImageEnhance, ImageFilter, ImageOps
# import pytesseract
# import io
# import cv2
import numpy as np
import re
# from pyzxing import BarCodeReader
from typing import Dict, List
import easyocr
# from pyzbar.pyzbar import decode
from fastapi.responses import JSONResponse
app = FastAPI()

reader = easyocr.Reader(['en'])  
pattern = re.compile(r'\b\w{5}-\w{3}-\w{4}\b')

@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        image = Image.open(io.BytesIO(contents))

        results = reader.readtext(np.array(image))

        # Format the results
        matched_texts = []
        for (bbox, text, prob) in results:
            matches = pattern.findall(text)
            for match in matches:
                # matched_texts.append({
                #     "matched_text": match,
                #     "bbox":  [int(coord) for point in bbox for coord in point],
                #     "probability": float(prob)  # 
                # })
                return {"extracted text: ": match}

        # return JSONResponse(content=matched_texts)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500) 
    
# def preprocess_image(image: Image.Image) -> np.ndarray:
#     try:
        
#         image = image.convert('L')

#         image_np = np.array(image)

#         # Gaussian Blur to reduce noise
#         image_np = cv2.GaussianBlur(image_np, (5, 5), 0)

#         # Adaptive Thresholding
#         image_np = cv2.adaptiveThreshold(image_np, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

#         # Morphological operations to remove noise
#         kernel = np.ones((1, 1), np.uint8)
#         image_np = cv2.dilate(image_np, kernel, iterations=1)
#         image_np = cv2.erode(image_np, kernel, iterations=1)

#         # Convert back to PIL image
#         image = Image.fromarray(image_np)

#         # Enhance contrast
#         enhancer = ImageEnhance.Contrast(image)
#         image = enhancer.enhance(2)

#         # Adjust brightness
#         enhancer = ImageEnhance.Brightness(image)
#         image = enhancer.enhance(1.5)

#         # Sharpening
#         image = image.filter(ImageFilter.SHARPEN)
#         return image

#     except Exception as e:
#         raise ValueError(f"Error in preprocessing image: {str(e)}")
    
# @app.post("/scan-barcode/")
# async def scan_barcode(file: UploadFile = File(...)) -> Dict[str, List[str]]:
#     # Read the image file
#     contents = await file.read()
#     nparr = np.frombuffer(contents, np.uint8)
#     image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#     # Decode the barcodes in the image
#     barcodes = decode(image)
#     barcode_map = {}

#     for barcode in barcodes:
#         barcode_data = barcode.data.decode("utf-8")
#         barcode_type = barcode.type
#         if barcode_type not in barcode_map:
#             barcode_map[barcode_type] = []
#         barcode_map[barcode_type].append(barcode_data)

#     return barcode_map

# def scan_barcode(image: Image.Image)-> dict:
#     # Read the image file
#     # nparr = np.frombuffer(image, np.uint8)
#     # image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#     # Decode the barcodes in the image
#     barcodes = decode(image)
#     results = []

#     for barcode in barcodes:
#         barcode_data = barcode.data.decode("utf-8")
#         barcode_type = barcode.type
#         results.append({"data": barcode_data, "type": barcode_type})

#     return {"barcodes": results}





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
