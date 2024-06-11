FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    pkg-config \
    poppler-utils
    
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

ENV NAME FastAPI

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
