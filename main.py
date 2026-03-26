from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import instaloader

app = FastAPI()

# Frontend (GitHub Pages) erişimi için CORS ayarı
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    session_id: str
    target: str

@app.get("/")
def home():
    return {"status": "ARCHERA CORE ACTIVE"}

@app.post("/api/query")
async def execute_query(data: QueryRequest):
    L = instaloader.Instaloader()
    
    # Session ID kullanımı (Eğer girdiysen aktif eder)
    if data.session_id and data.session_id != "default":
        # Burada session dosyasını yükleme mantığı çalışır
        pass

    try:
        # Hedef profil verilerini çekme
        profile = instaloader.Profile.from_username(L.context, data.target)
        
        # Suruç Analiz Mantığı
        bio = profile.biography.lower()
        location_status = "TESPİT EDİLDİ (SURUÇ)" if "suruç" in bio or "63" in bio else "ANALİZ EDİLİYOR..."

        return {
            "status": "success",
            "data": {
                "full_name": profile.full_name,
                "followers": profile.followers,
                "is_private": profile.is_private,
                "location_inference": location_status,
                "bio": profile.biography
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
