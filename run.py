
import requests
from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent
import csv


def get_html(url):#получение содержимого страницы
    try:
        response = requests.get(
            url, headers={'User-Agent': FakeUserAgent().chrome})
        response.raise_for_status()
        html = response.content
        return html
    except (requests.RequestException, ValueError):
        print('Что-то пошло не так')
        return False


def get_information():# получаем информацию о компании
    html = get_html('https://www.list-org.com/company/486813')
    soup = BeautifulSoup(html, 'html.parser')
    company_data = soup.find('table')
    full_name = soup.find('a', text=True)
    full_name = full_name.text
    titles = ['Полное юридическое наименование']
    items = [full_name]
    others = company_data.findAll('td')
    for i in range(0, len(others), 2):
        title = others[i].text
        titles.append(title)
    for j in range(1, len(others), 2):
        item = others[j].text
        items.append(item)
    company = dict(zip(titles, items))
    with open('company_data.csv', 'a', encoding='utf8', newline='') as output:
        f = csv.writer(output, delimiter=';')
        f.writerow(items)  # первый вариант
    return company

if __name__ == "__main__":
    get_information()

'''
company=get_information()
with open('company_data_2.csv', 'a', encoding='utf8') as output:
    [output.write('{0},{1}\n'.format(key, value))
     for key, value in company.items()]  # бонусный вариант, c полями'''
