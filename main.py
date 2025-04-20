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
    
    # حفظ الملف الصوتي
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # إرسال بيانات تجريبية للسيرفر الأول (تعديل لاحقًا)
    payload = {
        "time": 45.0,
        "sound_level": 0.22
    }

    try:
        response = requests.post(
            "https://echo-api-ceeq.onrender.com/predict",
            json=payload
        )
        prediction_result = response.json()
        message = "تم توصيل تشجيعك بنجاح!"
    except Exception as e:
        prediction_result = {"error": "تعذر الاتصال بالسيرفر الأول", "details": str(e)}
        message = "تم رفع الصوت لكن لم يتم توصيله للملعب"

    return JSONResponse(content={
        "message": message,
        "prediction": prediction_result
    })