from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import io
import re

app = FastAPI()

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)):
    try:
        # Read and load the image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # Use OCR to extract text
        extracted_text = pytesseract.image_to_string(image)

        # Look for multiplication problem, e.g., 12345678 * 87654321
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
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
