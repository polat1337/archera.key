import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from instagrapi import Client

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class LinkData(BaseModel):
    sessionid: str

class ActionData(BaseModel):
    target: str

cl = Client()

# --- 1. SESSION ID ILE SIZMA ---
@app.post("/api/v4/auth/link")
async def link_account(data: LinkData):
    try:
        cl.set_settings({"authorization_data": {"sessionid": data.sessionid}})
        cl.get_timeline_feed() # Test
        me = cl.account_info().dict()
        return {"status": "success", "user": me['username'], "message": "TUNEL ACILDI!"}
    except Exception as e:
        return {"status": "error", "message": "Session ID Gecersiz!"}

# --- 2. OTOMASYON: TAKIP ET ---
@app.post("/api/v4/action/follow")
async def follow_target(data: ActionData):
    try:
        user_id = cl.user_id_from_username(data.target)
        cl.user_follow(user_id)
        return {"status": "success", "message": f"@{data.target} takip edildi."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- 3. OTOMASYON: STORY INDIR ---
@app.post("/api/v4/action/stories")
async def get_stories(data: ActionData):
    try:
        user_id = cl.user_id_from_username(data.target)
        stories = cl.user_stories(user_id)
        urls = [s.video_url if s.media_type == 2 else s.thumbnail_url for s in stories]
        return {"status": "success", "urls": urls}
    except Exception as e:
        return {"status": "error", "message": str(e)}
