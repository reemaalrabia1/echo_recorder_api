from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
import requests

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    
    # حفظ الملف
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # إرسال بيانات تجريبية للسيرفر الأول
    payload = {
        "time": 45.0,
        "sound_level": 0.22
    }

    try:
        response = requests.post(
            "https://رابط-السيرفر-الأول.onrender.com/predict",  # غيّري الرابط هنا
            json=payload
        )
        prediction_result = response.json()
    except Exception as e:
        prediction_result = {"error": "تعذر الاتصال بالسيرفر الأول", "details": str(e)}

    return JSONResponse(content={
        "message": "تم رفع الملف بنجاح",
        "filename": file.filename,
        "prediction": prediction_result
    })