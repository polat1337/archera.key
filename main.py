from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import instaloader
import os

app = FastAPI()

# CORS Ayarları - Tarayıcı engellini kaldırmak için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    session_id: str
    target: str

@app.get("/")
async def home():
    return {"status": "ARCHERA CORE ACTIVE", "message": "Sistem Online Reis"}

@app.post("/api/query")
async def execute_query(data: QueryRequest):
    L = instaloader.Instaloader()
    
    # KRİTİK NOKTA: Session ID (Cookie) Kullanımı
    if data.session_id and data.session_id != "default":
        try:
            # Instagram'a "Ben bu kullanıcıyım" diyoruz
            L.context._session.cookies.set("sessionid", data.session_id)
            # Gerçek bir tarayıcı gibi davranması için User-Agent
            L.context.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        except Exception as e:
            print(f"Cookie hatası: {e}")

    try:
        # Profili çekmeye çalış
        profile = instaloader.Profile.from_username(L.context, data.target)
        
        # Suruç Analiz Algoritması
        bio = profile.biography.lower()
        suruc_keywords = ["suruç", "63", "şanlıurfa", "urfa", "suruc"]
        is_suruc = any(word in bio for word in suruc_keywords)
        
        location_status = "TESPİT EDİLDİ (SURUÇ) 🔥" if is_suruc else "ANALİZ EDİLİYOR..."

        return {
            "status": "success",
            "data": {
                "full_name": profile.full_name,
                "followers": profile.followers,
                "is_private": profile.is_private,
                "location_inference": location_status,
                "bio": profile.biography,
                "profile_pic": profile.profile_pic_url
            }
        }
    except Exception as e:
        # Hata mesajını detaylandırıyoruz
        error_msg = str(e)
        if "404" in error_msg:
            error_msg = f"Profil ({data.target}) bulunamadı veya Instagram engelledi (Yeni Session ID deneyin)."
        elif "401" in error_msg:
            error_msg = "Giriş hatası! Session ID geçersiz."
            
        raise HTTPException(status_code=400, detail=error_msg)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
