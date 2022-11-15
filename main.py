from hh_privy_councilor.api_client import HHAPIClient
from hh_privy_councilor.keyskills_analyzer import KeySkillsAnalyzer
from hh_privy_councilor.vacancy_dataclasses import Vacancies
import json

search_skills = [
    'django',
]

client = HHAPIClient(search_skills)
vacancies = client.compose_vacancies()


skills_postfix = '_'.join(search_skills)


with open(f'vacancies_data/vacancies_{skills_postfix}.json', 'w') as f:
    f.write(vacancies.json(indent=4, ensure_ascii=False))

# with open(f'vacancies_data/vacancies_{skills_postfix}.json') as f:
#     data = json.load(f)
#     vacancies = Vacancies(**data)

analyzer = KeySkillsAnalyzer(vacancies)

for item in sorted(analyzer.count_key_skills_frequency().items(), key=lambda x: x[1]):
    print(item)
# print(analyzer.count_key_skills_frequency())

