from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from instagrapi import Client
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Veri Modelleri
class QueryModel(BaseModel):
    query: str
    owner: str

class AuthModel(BaseModel):
    platform: str
    username: str
    password: str

@app.get("/")
def home():
    return {"status": "ARCHERA SYSTEM ONLINE", "mode": "Shadow V4"}

# SORGULAMA MOTORU
@app.post("/api/v4/sorgu")
async def run_osint(data: QueryModel):
    target_user = data.query.replace("@", "").strip()
    return {
        "status": "success",
        "targets": [
            {
                "username": target_user,
                "name": f"{target_user.capitalize()} Analiz Edildi",
                "location": "Suruc / Merkez",
                "leaks": [{"type": "Durum", "data": "Baglanti Basarili"}],
                "stories": ["https://via.placeholder.com/150"],
                "ai_report": f"{target_user} icin derin tarama aktif."
            }
        ]
    }

# GERCEK INSTAGRAM LOGIN (KRITIK BOLGE)
@app.post("/api/v4/auth/link")
async def link_account(data: AuthModel):
    if data.platform == "Instagram":
        cl = Client()
        try:
            # Burasi gercek giris denemesi yapar
            cl.login(data.username, data.password)
            user_info = cl.user_info_by_username(data.username)
            return {
                "status": "success", 
                "message": f"{data.username} basariyla tunellendi.",
                "account_id": user_info.pk
            }
        except Exception as e:
            return {"status": "error", "message": f"Giris Hatasi: {str(e)}"}
    return {"status": "error", "message": "Platform desteklenmiyor."}
