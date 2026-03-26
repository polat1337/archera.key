from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import instaloader
import os

app = FastAPI()

# CORS Ayarları - Duvarları tamamen yıkıyoruz
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
    # UptimeRobot buraya bakınca 200 OK alacak ve sistem 'UP' görünecek
    return {"status": "ARCHERA CORE ACTIVE", "heartbeat": "stable"}

@app.post("/api/query")
async def execute_query(data: QueryRequest):
    L = instaloader.Instaloader()
    
    if data.session_id and data.session_id != "default":
        L.context._session.cookies.set("sessionid", data.session_id)
        L.context.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

    try:
        profile = instaloader.Profile.from_username(L.context, data.target)
        
        bio = profile.biography.lower()
        is_suruc = any(word in bio for word in ["suruç", "63", "şanlıurfa", "urfa", "suruc"])
        
        return {
            "status": "success",
            "data": {
                "full_name": profile.full_name,
                "followers": profile.followers,
                "following": profile.followees, # Takip edilen eklendi
                "is_private": profile.is_private,
                "location_inference": "TESPİT EDİLDİ (SURUÇ) 🔥" if is_suruc else "ANALİZ EDİLİYOR...",
                "bio": profile.biography,
                "profile_pic": profile.profile_pic_url # Fotoğraf URL'si eklendi
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
