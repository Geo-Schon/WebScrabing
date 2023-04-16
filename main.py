import requests
import os
from bs4 import BeautifulSoup as bs
from fake_headers import Headers
from tqdm import tqdm
import re
import json


def get_headers():
    return Headers(browser="chrome", os="win").generate()


def main_page_search(url):
    hh_main_html = requests.get(url=url, headers=get_headers()).text
    hh_main_soup = bs(hh_main_html, "lxml")
    tag_all_vacancy = hh_main_soup.find_all("div", class_="serp-item")
    return tag_all_vacancy


def job_search(tag_vacancy):
    link_vacancy = tag_vacancy.find("a", class_="serp-item__title")["href"]
    if tag_vacancy.find("span", class_="bloko-header-section-3") is None:
        salary_vacancy = f"Зарлата не указана"
    else:
        salary_vacancy = tag_vacancy.find('span', class_='bloko-header-section-3').text
    name_company_vacancy = tag_vacancy.find("a", "bloko-link bloko-link_kind-tertiary").text
    title = tag_vacancy.find('a', class_='serp-item__title').text
    tag_description = requests.get(url=link_vacancy, headers=get_headers()).text
    tag_description_soup = bs(tag_description, "lxml")
    description_vacancy = tag_description_soup.find("div", class_="g-user-content").text
    return {
        "name": title,
        "link": link_vacancy,
        "salary": salary_vacancy,
        "name_company": name_company_vacancy,
        "description": description_vacancy
    }


def query_search(main_page):
    parsed_data = []
    for tag_vacancy in tqdm(main_page):
        jobs_found = job_search(tag_vacancy)
        jobs_desc = jobs_found["description"]
        pattern = re.findall(
            r"([Dd]jango.*[Ff]lask)|([Ff]lask.*[Dd]jango)|([Ff]lask.*\s*.*[Dd]jango)", jobs_desc,)
        if pattern != []:
            _ = jobs_found.pop("description", None)
            parsed_data.append(jobs_found)
    return parsed_data


def write_file(file_name, total_list):
    current = os.getcwd()
    full_path = os.path.join(current, file_name)
    with open(full_path, "w", encoding="utf=8") as w:
        json.dump(total_list, w, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main_page = main_page_search("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2")
    result = query_search(main_page)
    write_file("jobs.json", result)
