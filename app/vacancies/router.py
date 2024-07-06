from typing import List, Optional
from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
import requests 
from app.utils import convert_gross
from app.vacancies.schemas import SVacancy, VacancySearchArgs 
from app.vacancies.constants import API_URL_VACANCIES, area_dict, experience_dict, schedule_dict
from app.vacancies.dao import VacancyDAO 

router = APIRouter(
    prefix = "/vacancies",
    tags=["Поиск Вакансий"]
)

@router.get("/search", response_model=List[SVacancy])
def get_vacancy(args: VacancySearchArgs = Depends()):
    params = {
        "text": args.keyword,
        "per_page": args.pages,
    }

    if args.area:
        for area in args.area:
            try:
                params["area"] = params.get("area", []) + [area_dict[area]]
            except KeyError:
                raise HTTPException(status_code=400, detail=f"Invalid area: {area}")

    if args.experience:
        for experience in args.experience:
            try:
                params["experience"] = params.get("experience", []) + [experience_dict[experience]]
            except KeyError:
                raise HTTPException(status_code=400, detail=f"Invalid experience: {experience}")

    if args.schedule:
        for schedule in args.schedule:
            try:
                params["schedule"] = params.get("schedule", []) + [schedule_dict[schedule]]
            except KeyError:
                raise HTTPException(status_code=400, detail=f"Invalid schedule: {schedule}")

    headers = {
        "User-Agent": "Your User Agent",
    }

    response = requests.get(API_URL_VACANCIES, params=params, headers=headers)
    data = response.json()
    vacancies = data.get("items", [])
    result = []
    for vacancy in vacancies:
        salary = vacancy.get("salary")
        from_to = {"from": None, "to": None}
        if salary:
            is_gross = vacancy["salary"].get("gross")
            for k in from_to.keys():
                if salary[k] is not None:
                    _value = convert_gross(is_gross)
                    from_to[k] = int(_value * salary[k])

        result.append(SVacancy(
            title=vacancy.get("name"),
            company=vacancy.get("employer", {}).get("name"),
            url=vacancy.get("alternate_url"),
            salary_from=from_to["from"],
            salary_to=from_to["to"],
            experience=vacancy.get("experience", {}).get("name", ""),
            area=vacancy.get("area", {}).get("name", ""),
            schedule=vacancy.get("schedule", {}).get("name", "")
        ))
    return result

@router.post("/add", status_code=201)
async def add_vacancies_to_db(vacancies: List[SVacancy]):
    for vacancy in vacancies:
        await VacancyDAO.add(**vacancy.model_dump())
    return {"message": "Vacancies added successfully"}


@router.get("/db-search", response_model=List[SVacancy])
async def get_vacancies_from_db(
    keyword: Optional[str] = Query(None),
    area: Optional[List[str]] = Query(None),
    experience: Optional[List[str]] = Query(None),
    schedule: Optional[List[str]] = Query(None)
):
    filter_by = {}
    
    if keyword:
        filter_by['title'] = keyword
    
    if area:
        filter_by['area'] = area
    
    if experience:
        filter_by['experience'] = experience
    
    if schedule:
        filter_by['schedule'] = schedule

    vacancies = await VacancyDAO.find_all(**filter_by)
    
    return [SVacancy(
        title=vacancy.title,
        company=vacancy.company,
        area=vacancy.area,
        experience=vacancy.experience,
        schedule=vacancy.schedule,
        url=vacancy.url,
        salary_from=vacancy.salary_from,
        salary_to=vacancy.salary_to,
    ) for vacancy in vacancies]