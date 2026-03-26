import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Menü Veritabanı (Render her kapandığında sıfırlanır, ileride DB'ye bağlarız)
menu_db = [
    {"id": "mod-home", "label": "GİRİŞ", "icon": "fas fa-user-shield"},
    {"id": "mod-db", "label": "SORGULA", "icon": "fas fa-search"}
]

class MenuEntry(BaseModel):
    id: str
    label: str
    icon: str

@app.get("/api/v4/menus")
async def get_menus():
    return menu_db

@app.post("/api/v4/menus/add")
async def add_menu(m: MenuEntry):
    menu_db.append(m.dict())
    return {"status": "success"}
