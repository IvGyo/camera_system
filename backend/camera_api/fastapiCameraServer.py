import os
import sqlite3
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import FileResponse

# --- ДЕФИНИРАНЕ НА ПЪТИЩАТА НАЙ-ОТГОРЕ ---
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "plates.db")
STATIC_DIR = os.path.join(APP_DIR, "static")

# --- Управление на базата данни ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS plates (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       plate_num TEXT,
                       confidence INTEGER,
                       timestamp TEXT,
                       is_whitelist BOOLEAN,
                       active_from TEXT,
                       active_to TEXT)''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()

# ВАЖНО: Променете "/YOUR_APP_SUBDIRECTORY/" с реалния път на сървъра
app = FastAPI(root_path="/YOUR_APP_SUBDIRECTORY/")

# --- Pydantic модели ---
class PlateData(BaseModel):
    plate_num: str
    confidence: int
    timestamp: str

class WhitelistData(BaseModel):
    plate_num: str
    active_from: str
    active_to: str

# ... (Тук поставете всичките си функции като add_plate, is_plate_whitelisted и всички @app.post/@app.get адреси) ...
# Пример:
@app.get("/plates")
async def get_plates(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, plate_num, confidence, timestamp, is_whitelist, active_from, active_to FROM plates ORDER BY id DESC")
    plates_data = cursor.fetchall()
    plates = [dict(row) for row in plates_data]
    return {"plates": plates}

# --- Код за сервиране на React ---
app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="assets")

@app.get("/{full_path:path}", response_class=FileResponse)
async def serve_react_app(full_path: str):
    return os.path.join(STATIC_DIR, "index.html")

# --- Код за стартиране ---
if __name__ == "__main__":
    uvicorn.run("fastapiCameraServer:app", host="0.0.0.0", port=8000, reload=True)
