from sqlalchemy import Column, Integer, String
from app.database import Base

class Vacancy(Base):
    __tablename__ = "vacancies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    area = Column(String, nullable=False)
    experience = Column(String, nullable=False)
    schedule = Column(String, nullable=False)
    url = Column(String, nullable=False)
    salary_from = Column(Integer, nullable=True)
    salary_to = Column(Integer, nullable=True)