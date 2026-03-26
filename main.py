import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from instagrapi import Client

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Tüm giriş yöntemlerini kapsayan model
class AuthData(BaseModel):
    username: str = ""
    password: str = ""
    verification_code: str = ""
    sessionid: str = ""

cl = Client()

@app.post("/api/v4/auth/link")
async def link_account(data: AuthData):
    try:
        # YÖNTEM 1: SESSION ID İLE BYPASS (EN SAĞLAMI)
        if data.sessionid:
            cl.set_settings({"authorization_data": {"sessionid": data.sessionid}})
            cl.get_timeline_feed() # Bağlantı testi
            return {"status": "success", "message": "SESSION ILE SIZILDI!"}

        # YÖNTEM 2: ONAY KODU / BENDİM TEYİDİ
        if data.verification_code == "confirmed" or data.verification_code.isdigit():
            if data.verification_code.isdigit():
                cl.checkpoint_login(data.verification_code)
            else:
                cl.login(data.username, data.password)
            return {"status": "success", "message": "TUNEL SABITLENDI!"}

        # YÖNTEM 3: NORMAL GİRİŞ
        cl.login(data.username, data.password)
        return {"status": "success", "message": "GIRIS BASARILI!"}

    except Exception as e:
        err = str(e).lower()
        if "challenge" in err or "checkpoint" in err:
            try: cl.challenge_resolve(cl.last_json)
            except: pass
            return {"status": "challenge", "message": "Instagram Onay Bekliyor! Uygulamadan 'Bendim' de veya kodu gir."}
        return {"status": "error", "message": str(e)}

@app.post("/api/v4/sorgu")
async def run_osint(target: dict):
    # Burası tünel açıldıktan sonra gerçek veri çekecek kısım
    return {"status": "success", "data": "Hedef Analiz Ediliyor..."}
