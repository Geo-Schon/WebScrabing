import requests
import csv
from bs4 import BeautifulSoup
from fake_headers import Headers

header = Headers(browser='firefox', os='win')
base_url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area'
request = requests.get(f'{base_url}', headers=header.generate()).text
soup = BeautifulSoup(request, 'lxml')

urls = []
pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
count_pages = int(pagination[-1].text)
for i in range(count_pages):
    url = f'https://spb.hh.ru/search/vacancy?text=python&area=1&area={i}'
    if url not in urls:
        urls.append(url)
        print(url)

parsed_data = []
divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
for div in divs:
    vac = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})
    title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
    href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
    company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
    description1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
    description2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
    description = description1 + description2
    parsed_data.append({
        'title': title,
        'href': href,
        'company': company,
        'description': description})

with open('jobs.csv', 'w', newline='') as file:
    a_pen = csv.writer(file, delimiter=',')
    a_pen.writerow(('Название вакансии', 'URL', 'Название комании', 'Описание'))
    for job in parsed_data:
            a_pen.writerow((job['title'], job['href'], job['company'], job['description']))

print(parsed_data)
