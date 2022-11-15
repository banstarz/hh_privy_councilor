from pydantic import BaseModel
from typing import Optional


class Vacancy(BaseModel):
    vacancy_id: int
    name: Optional[str]
    city: Optional[str]
    salary_from: Optional[float]
    salary_to: Optional[float]
    salary_currency: Optional[str]
    salary_gross: Optional[bool]
    experience: Optional[str]
    description: Optional[str]
    key_skills: Optional[list[str]]
    employer: Optional[str]
    published_at: str
    created_at: str
    initial_created_at: str
    has_test: Optional[bool]


class Vacancies(BaseModel):
    search_skills: list[str]
    vacancies: list[Vacancy]

