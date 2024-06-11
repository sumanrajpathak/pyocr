from fastapi import FastAPI, File, UploadFile
from PIL import Image
import pytesseract
import io
import cv2

app = FastAPI()


@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    contents = await file.read()
    # pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
    image = Image.open(io.BytesIO(contents))
    text = pytesseract.image_to_string(image)
    
    return {"extracted_text": text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
