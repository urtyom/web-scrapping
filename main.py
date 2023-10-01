import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json
import re


headers_gen = Headers(os='win', browser='chrome')

response_main = requests.get(
  'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2',
  headers=headers_gen.generate()
  )

html_data = response_main.text
main_soup = BeautifulSoup(html_data, 'lxml')
vacancy_list_r = main_soup.find('div', class_='vacancy-serp-content')
vacancy_list_c = main_soup.find('div', id='a11y-main-content')
vacancy_tags = vacancy_list_c.find_all('div', class_='serp-item')

vacancy_tag_list = []

for vac in vacancy_tags:
  layout = vac.find('div', class_='vacancy-serp-item__layout')
  body = layout.find('div', class_='vacancy-serp-item-body')
  main_info = body.find('div', class_='vacancy-serp-item-body__main-info')
  div = main_info.find('div')
  h3 = div.find('h3')
  span = h3.find('span')
  a = vac.find('a')
  href = a['href']

  response_href_html = requests.get(
    href,
    headers=headers_gen.generate()
    )

  href_html_data = response_href_html.text
  response_href_soup = BeautifulSoup(href_html_data, 'lxml')
  href_info = response_href_soup.find('script', type='application/ld+json')
  decoded = json.loads(href_info.text)
  dur = decoded['description']
  pattern_1 = r"Django|Flask|django|flask"
  find_word = re.findall(pattern_1, dur)

  if find_word != []:
    vacancy_tag_dict = {}
    span_price = div.find('span', class_='bloko-header-section-2')
    if span_price != None:
      price = span_price.text
    else:
      price = 'зп не указана'
    name = decoded['hiringOrganization']['name']
    city = decoded['jobLocation']['address']['addressLocality']
    vacancy_tag_dict[href] = [name, city, price]

    vacancy_tag_list.append(vacancy_tag_dict)

with open('new_file_json', 'w', encoding='utf8') as f:
  json.dump(vacancy_tag_list, f)
