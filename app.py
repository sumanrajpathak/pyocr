from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
import numpy as np
import re
import easyocr
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request


app = FastAPI()

reader = easyocr.Reader(['en'])  
pattern = re.compile(r'\b[A-Za-z0-9]{5}-[A-Za-z0-9]{3}-[A-Za-z0-9]{3,5}\b')
templates = Jinja2Templates(directory="templates")

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    try:
        if(file.content_type != "image/jpeg" and file.content_type != "image/png"):
            return JSONResponse(content={"error": "No file uploaded"}, status_code=422)
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        results = reader.readtext(np.array(image))
        extracted_text = ' '.join([res[1] for res in results])
        matches = pattern.findall(extracted_text)
        return JSONResponse(content={"data": matches})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=422)
     
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})   
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
