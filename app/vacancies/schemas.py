from typing import List, Optional
from fastapi import Query
from pydantic import BaseModel 

class SVacancy(BaseModel):
    title: str
    company: str
    area: str
    experience: str
    schedule: str
    url: str
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None

class VacancySearchArgs():
    def __init__(
            self, 
            keyword: str, 
            area: Optional[List[str]] = Query(None),
            experience: Optional[List[str]] = Query(None),
            schedule: Optional[List[str]] = Query(None),
            pages: Optional[int] = None,
    ):
        
        self.keyword = keyword 
        self.area = area 
        self.experience = experience
        self.schedule = schedule 
        self.pages = pages
