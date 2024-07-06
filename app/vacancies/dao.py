from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.vacancies.models import Vacancy

from sqlalchemy import select 

class VacancyDAO(BaseDAO):
    model = Vacancy