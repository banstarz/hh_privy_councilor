from collections import Counter
from .vacancy_dataclasses import Vacancies
import re


class KeySkillsAnalyzer:

    def __init__(self, vacancies: Vacancies):
        self.vacancies = vacancies

    def count_key_skills_frequency(self) -> Counter:
        skills = []

        for vacancy in self.vacancies.vacancies:
            for key_skill in vacancy.key_skills:
                skills.append(key_skill)

        key_skills_frequency = Counter(skills)

        return key_skills_frequency

    def parse_skill_from_description(self) -> list[str]:
        skills = []
        pattern = r'[a-zA-Z&]+'
        for vacancy in self.vacancies.vacancies:
            vacancy_key_skills = set(re.findall(pattern, vacancy.description))
            skills.extend(vacancy_key_skills)


