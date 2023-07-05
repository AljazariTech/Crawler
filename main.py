import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv

load_dotenv()



def get_product_info(url, headers):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_list = []

    products = soup.find_all('div', {'class': 'ModelInfo'})  # Adjust according to the webpage structure
    for product in products:
        title = product.find('a', {'class': 'ModelName'}).text  # Get product title
        prices = product.find('div', {'class': 'PricesTxt'}).find_all('strong')  # Get product prices
        lowest = int(prices[0].text.replace(',', ''))
        if len(prices) > 1:
            highest = int(prices[1].text.replace(',', ''))
        else:
            highest = lowest

        product_list.append({
            "title": title,
            "lowest": lowest,
            "highest": highest
        })

    return product_list


def get_all_products(base_url, category):
    page_num = 1
    all_products = []

    while True:
        url = f'{base_url}sog={category}&pageinfo={page_num}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        }
        products = get_product_info(url, headers)
        if not products:
            break
        all_products.extend(products)
        page_num += 1

    return all_products


category = "e-fridge"  # Update this based on the category you're interested in
base_url = os.getenv('BASE_URL')
products = get_all_products(base_url, category)
print(json.dumps(products, ensure_ascii=False))
#ZapCrawler(category, page)
