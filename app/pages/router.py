from typing import Optional
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_cache.decorator import cache
 
router = APIRouter(
    prefix = "",
    tags = ["Фронтенд"]
)

clients = []
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/db", response_class=HTMLResponse)
async def get_db_page(request: Request):
    return templates.TemplateResponse("db.html", {"request": request})
