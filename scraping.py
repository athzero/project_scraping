import requests
from bs4 import BeautifulSoup
import json
import time

# Базовый URL сайта
base_url = "http://quotes.toscrape.com"

# Функция для получения информации об авторе
def get_informations(link):
    author_url = base_url + link
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }
    response = requests.get(author_url, headers=headers)
    # Проверяем успешность запроса
    if response.status_code != 200:
        print(f"Failed to retrieve data from {author_url}")
        return {
            "born_date": "Unknown",
            "born_location": "Unknown",
            "description": "No description available"
        }
    soup = BeautifulSoup(response.text, "html.parser")
    born_date = soup.find("span", class_="author-born-date")
    born_location = soup.find("span", class_="author-born-location")
    description = soup.find("div", class_="author-description")
    
    return {
        "born_date": born_date.get_text(strip=True) if born_date else "Unknown",
        "born_location": born_location.get_text(strip=True) if born_location else "Unknown",
        "description": description.get_text(strip=True) if description else "No description available"
    }

# Функция для получения цитат и авторов с главной страницы
def get_quotes():
    quotes_data = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }
    page_url = "/page/1/"
    
    while page_url:
        # Отправляем запрос
        response = requests.get(base_url + page_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")
        for quote in quotes:
            text = quote.find("span", class_="text").get_text(strip=True)
            author = quote.find("small", class_="author").get_text(strip=True)
            author_link = quote.find("a")["href"]
            
            # Получаем информацию об авторе
            author_data = get_informations(author_link)
            quotes_data.append({
                "text": text,
                "author": author,
                "born_date": author_data["born_date"],
                "born_location": author_data["born_location"],
                "description": author_data["description"]
            })
            time.sleep(10)
        
        # Проверяем наличие следующей страницы
        next_button = soup.find("li", class_="next")
        if next_button:
            page_url = next_button.find("a")["href"]
        else:
            page_url = None
    
    return quotes_data

if __name__ == "__main__":
    quotes = get_quotes()
    
    # Сохранение данных в JSON-файл
    with open("quotes.json", "w", encoding="utf-8") as file:
        json.dump(quotes, file, ensure_ascii=False, indent=4)
