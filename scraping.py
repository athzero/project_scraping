import requests
from bs4 import BeautifulSoup
import json

def parse_quotes_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes_data = []
    
    quotes = soup.find_all('div', class_='quote')
    for quote in quotes:
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
        quotes_data.append({
            'text': text,
            'author': author,
            'tags': tags
        })
    
    return quotes_data

url = 'https://quotes.toscrape.com/page/1/'
all_quotes = []

while url:
    page_quotes = parse_quotes_page(url)
    all_quotes.extend(page_quotes)

    # Проверка наличия ссылки на следующую страницу
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    next_button = soup.find('li', class_='next')
    if next_button:
        next_page = next_button.find('a')['href']
        url = f'https://quotes.toscrape.com{next_page}'
    else:
        url = None
with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(all_quotes, f, ensure_ascii=False, indent=4)