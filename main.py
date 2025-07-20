from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OCR_SPACE_API_KEY = "helloworld"  # Free API key provided by ocr.space for testing

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)):
    try:
        # Read file contents
        image_bytes = await file.read()

        # Send image to OCR.space API
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": (file.filename, image_bytes)},
            data={"apikey": OCR_SPACE_API_KEY, "language": "eng"}
        )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="OCR API failed")

        result_json = response.json()
        parsed_text = result_json["ParsedResults"][0]["ParsedText"]

        # Extract multiplication expression
        match = re.search(r'(\d{8})\s*[*xX×]\s*(\d{8})', parsed_text)
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
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
