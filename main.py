from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import re

app = FastAPI()

# Allow CORS (important for Swagger or frontend use)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OCR.space free key for testing
OCR_SPACE_API_KEY = "helloworld"  # Do not change this

@app.get("/")
def root():
    return {"message": "POST an image to /captcha to extract and solve the multiplication problem."}

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)):
    try:
        # Read the uploaded image bytes
        image_bytes = await file.read()

        # Call OCR.space API
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": (file.filename, image_bytes)},
            data={"apikey": OCR_SPACE_API_KEY, "language": "eng"}
        )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="OCR API failed")

        result_json = response.json()

        # Extract text from OCR
        parsed_text = result_json["ParsedResults"][0]["ParsedText"]
        print("OCR Text:", parsed_text)  # Debug in logs

        # Use flexible regex to extract multiplication of 6–10 digit numbers
        match = re.search(r'(\d{6,10})\s*[*xX××x]\s*(\d{6,10})', parsed_text)
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
        print(f"Error occurred: {e}")  # Show in Render logs
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
