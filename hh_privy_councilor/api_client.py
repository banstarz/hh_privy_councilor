import requests
import time
from loguru import logger
from .vacancy_dataclasses import Vacancy, Vacancies


DOMAIN = 'https://api.hh.ru'
VACANCIES = '/vacancies'
ARES = '/areas'
DICTIONARIES = '/dictionaries'


class HHAPIClient:

    def __init__(self, search_skills: list[str]):
        self.search_skills = search_skills
        self.links = []

    def compose_vacancies(self) -> Vacancies:
        list_of_vacancies = []

        self.get_all_vacancy_urls()

        for link in self.links:
            response = requests.get(link)
            response_dict = response.json()
            logger.info(f'Requested vacancy: response status: {response.status_code} response type: {type(response.json())}')
            logger.debug(f'Vacancy url {link}')

            list_of_vacancies.append(self.produce_vacancy_object(response_dict))

        vacancies_params = {
            'search_skills': self.search_skills,
            'vacancies': list_of_vacancies,
        }

        return Vacancies(**vacancies_params)

    def produce_vacancy_object(self, item: dict) -> Vacancy:
        vacancy_attrs = {
            'vacancy_id':           self.get_dict_item_by_path(item, 'id'),
            'name':                 self.get_dict_item_by_path(item, 'name'),
            'city':                 self.get_dict_item_by_path(item, 'area.name'),
            'salary_from':          self.get_dict_item_by_path(item, 'salary.from'),
            'salary_to':            self.get_dict_item_by_path(item, 'salary.to'),
            'salary_currency':      self.get_dict_item_by_path(item, 'salary.currency'),
            'salary_gross':         self.get_dict_item_by_path(item, 'salary.gross'),
            'experience':           self.get_dict_item_by_path(item, 'experience.name'),
            'description':          self.get_dict_item_by_path(item, 'description'),
            'key_skills':           [skill['name'] for skill in item.get('key_skills', [])],
            'employer':             self.get_dict_item_by_path(item, 'employer.name'),
            'published_at':         self.get_dict_item_by_path(item, 'published_at'),
            'created_at':           self.get_dict_item_by_path(item, 'created_at'),
            'initial_created_at':   self.get_dict_item_by_path(item, 'initial_created_at'),
            'has_test':             self.get_dict_item_by_path(item, 'has_test'),
        }

        return Vacancy(**vacancy_attrs)

    def get_all_vacancy_urls(self) -> None:
        search_text = ' '.join(self.search_skills)

        total_pages = 1
        current_page = 1
        params = {
            'text': search_text,
            'per_page': 100,
            'date_from': '2022-11-05'
        }

        logger.info(f'Started obtaining vacancies for {search_text}')

        while current_page <= total_pages:
            params.update({'page': current_page})
            response = requests.get(DOMAIN + VACANCIES, params=params)
            logger.info(f'Got vacancies: status: {response.status_code}  page: {current_page}  total_pages: {total_pages}')

            if response.status_code == 400:
                break

            if response.status_code != 200:
                logger.info(f'Got status {response.status_code} go to sleep for 2 seconds')
                time.sleep(2)
                continue

            response_dict = response.json()
            page_vacancy_urls = [item['url'] for item in response_dict['items']]
            self.links.extend(page_vacancy_urls)
            logger.info(f'Total links {len(self.links)}')
            current_page += 1
            total_pages = response_dict['pages']

    def get_dict_item_by_path(self, obj: dict, path: str):
        splitted_path = path.split('.', maxsplit=1)
        nested_obj = obj.get(splitted_path[0])
        if not nested_obj:
            return None

        if len(splitted_path) == 1:
            return obj.get(splitted_path[0])
        else:
            tail_path = splitted_path[1]
            return self.get_dict_item_by_path(nested_obj, tail_path)
