from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel

from typing import Optional 

from app.utils import convert_gross
from app.vacancies.router import router as router_vacancies
from app.pages.router import router as router_pages

app = FastAPI()

app.include_router(router_vacancies)
app.include_router(router_pages)