from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
import io
import re

app = FastAPI()

# Enable CORS so Swagger UI & browsers work without "Failed to fetch"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (can restrict if needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)):
    try:
        # Read image file bytes and open it
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # Extract text using OCR
        extracted_text = pytesseract.image_to_string(image)

        # Find 8-digit * 8-digit multiplication pattern
        match = re.search(r'(\d{8})\s*[*xX×]\s*(\d{8})', extracted_text)
        if not match:
            raise HTTPException(status_code=400, detail="No valid multiplication problem found in image.")

        num1 = int(match.group(1))
        num2 = int(match.group(2))
        result = num1 * num2

        return JSONResponse(content={
            "answer": result,
            "email": "23f2003455@ds.study.iitm.ac.in"
        })

    except Exception as e:
        print(f"Error occurred: {e}")  # This will show in Render logs
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
