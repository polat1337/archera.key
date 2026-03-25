import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from instagrapi import Client

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# En basit veri modeli
class AuthData(BaseModel):
    username: str
    password: str
    verification_code: str = ""

cl = Client()

@app.post("/api/v4/auth/link")
async def link_account(data: AuthData):
    try:
        # Eğer panelden doğrulama kodu gelmişse
        if data.verification_code:
            cl.checkpoint_login(data.verification_code)
            return {"status": "success", "message": "Kod onaylandi, tunel sabit!"}
        
        # İlk giriş denemesi
        cl.login(data.username, data.password)
        return {"status": "success", "message": "Giris basarili!"}

    except Exception as e:
        err = str(e)
        if "challenge_required" in err:
            try:
                cl.challenge_resolve(cl.last_json)
                return {"status": "challenge", "message": "Kod gonderildi."}
            except:
                return {"status": "error", "message": "Instagram onay bekliyor, telefona bak."}
        return {"status": "error", "message": err}

@app.post("/api/v4/sorgu")
async def sorgu(data: dict):
    return {"status": "success", "targets": [{"name": "Sistem Aktif"}]}
