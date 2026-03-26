from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import instaloader
import os

app = FastAPI()

# TÜM DÜNYAYA ERİŞİM İZNİ VERİYORUZ (CORS ERROR ÇÖZÜMÜ)
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
    try:
        profile = instaloader.Profile.from_username(L.context, data.target)
        
        bio = profile.biography.lower()
        location_status = "TESPİT EDİLDİ (SURUÇ)" if "suruç" in bio or "63" in bio else "ANALİZ EDİLİYOR..."

        return {
            "status": "success",
            "data": {
                "full_name": profile.full_name,
                "followers": profile.followers,
                "is_private": profile.is_private,
                "location_inference": location_status
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
