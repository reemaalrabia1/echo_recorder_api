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
        requests.post(
            "https://echo-api-ceeq.onrender.com/predict",
            json=payload
        )
        message = "شكرًا! صوتك وصل."
    except Exception:
        message = "شكرًا! صوتك وصل."  # حتى لو فشل الإرسال نعرض نفس الرسالة

    return JSONResponse(content={"message": message})