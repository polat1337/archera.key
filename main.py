import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from instagrapi import Client

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

cl = Client()
# Dinamik Menü Veritabanı (Başlangıç Ayarları)
menu_db = [
    {"id": "mod-home", "label": "GİRİŞ", "icon": "fas fa-user-shield"},
    {"id": "mod-db", "label": "SORGULA", "icon": "fas fa-search"}
]

class MenuEntry(BaseModel):
    id: str
    label: str
    icon: str

# --- MENÜ YÖNETİMİ ---
@app.get("/api/v4/menus")
async def get_menus(): return menu_db

@app.post("/api/v4/menus/add")
async def add_menu(m: MenuEntry):
    menu_db.append(m.dict())
    return {"status": "success"}

# --- INSTAGRAM & OTOMASYON ---
@app.post("/api/v4/ig/link")
async def ig_link(data: dict):
    try:
        cl.set_settings({"authorization_data": {"sessionid": data['sid']}})
        return {"status": "success", "user": cl.account_info().dict()['username']}
    except: return {"status": "error", "message": "Session Hatalı!"}
