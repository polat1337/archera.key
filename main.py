import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from instagrapi import Client

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class AuthModel(BaseModel):
    username: str
    password: str
    verification_code: str = ""

cl = Client()

@app.post("/api/v4/auth/link")
async def link_account(data: AuthModel):
    try:
        # Eğer panelden bir kod gelmişse, girişi kodla tamamla
        if data.verification_code:
            cl.checkpoint_login(data.verification_code)
            return {"status": "success", "message": "Kod onaylandi, hesap baglandi!"}
        
        # Normal giriş denemesi
        cl.login(data.username, data.password)
        return {"status": "success", "message": "Giris basarili!"}

    except Exception as e:
        error = str(e)
        if "challenge_required" in error:
            # Instagram'a "bize kod gönder" komutu veriyoruz
            cl.challenge_resolve(cl.last_json) 
            return {"status": "challenge", "message": "Instagram 6 haneli kod gonderdi. Kodu gir kanka."}
        return {"status": "error", "message": error}
