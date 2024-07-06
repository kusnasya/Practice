import asyncio
import json
import pytest
from sqlalchemy import insert 
from app.config import settings
from app.database import Base, async_session_maker, engine 

from app.vacancies.models import Vacancy

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metdata.create_all)

    def open_mock_json(model: str):
        with open("app/test/mock_{model}.json", "r") as file:
            return json.load(file)
        
    vacancies = open_mock_json("vacancies")

    async with async_session_maker() as session:
        add_vacancies = insert(Vacancy).values(vacancies)
        await session.execute(add_vacancies)

        await session.commit()

@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close