import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from instagrapi import Client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuthModel(BaseModel):
    platform: str
    username: str
    password: str

SESSION_FILE = "session.json"

@app.post("/api/v4/auth/link")
async def link_account(data: AuthModel):
    cl = Client()
    
    # 1. EGER ONCEDEN GIRIS YAPILDIYSA OTURUMU YUKLE
    if os.path.exists(SESSION_FILE):
        try:
            cl.load_settings(SESSION_FILE)
            print("Eski oturum yuklendi...")
        except:
            pass

    try:
        # 2. GIRIS YAPMAYI DENE
        cl.login(data.username, data.password)
        
        # 3. GIRIS BASARILIYSA OTURUMU KAYDET (BIR DAHAKI SEFERE SORMAZ)
        cl.dump_settings(SESSION_FILE)
        return {"status": "success", "message": "Tunel sabitlendi, giris basarili!"}

    except Exception as e:
        error_msg = str(e)
        # Challenge hatasi gelirse burasi calisir
        if "challenge_required" in error_msg:
            return {
                "status": "error", 
                "message": "Instagram guvenlik onayi bekliyor. Telefondan 'Bendim' dedikten 10 saniye sonra TEKRAR butona bas kanka."
            }
        return {"status": "error", "message": error_msg}

@app.post("/api/v4/sorgu")
async def run_osint(data: dict):
    return {"status": "success", "targets": [{"name": "ARCHERA SYSTEM ACTIVE", "location": "Suruc"}]}
