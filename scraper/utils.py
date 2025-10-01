# utils.py

import requests
import json
import pandas as pd
import numpy as np
import concurrent.futures
from time import sleep


class Scrape:
    def __init__(self, search, items):
        self.items = items
        self.proxy_available = []
        self.url = f'https://api.digikala.com/v1/search/?q={search}&page='
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'api.digikala.com',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
        }

    def send_request(self, page, proxy=None):
        """
        Send HTTP GET request to Digikala API for a specific page.
        If proxy is provided, use it.
        """
        try:
            sleep(2)  # Delay to avoid being blocked
            proxies = {'http': proxy, 'https': proxy} if proxy else None
            response = requests.get(self.url + f'{page}', headers=self.header, proxies=proxies, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'Failed to fetch page {page}: {e}')
            return {"data": {"products": []}}

    def get_data(self):
        """
        Scrape product data for the given search term and number of items.
        Returns a pandas DataFrame.
        """
        end_page = int(np.ceil(self.items / 20))
        end_item = self.items - (end_page - 1) * 20
        page = 1
        data = self.send_request(page)
        data_final = []
        index = 20

        while data['data']['products']:
            max_len = len(data['data']['products'])
            if page == end_page:
                index = end_item if end_item < max_len else max_len

            for i in range(0, int(index)):
                try:
                    product = data['data']['products'][i]
                    title = product['title_fa']
                    product_url = 'https://www.digikala.com/' + product['url']['uri']
                    category = product['data_layer']['category']
                    image_url = product['images']['main']['url'][0]
                    rating = product['rating']['rate']
                    price = product['default_variant']['price']['selling_price']
                    data_final.append({
                        'title': title,
                        'product_url': product_url,
                        'category': category,
                        'image_url': image_url,
                        'rating': rating,
                        'price': price
                    })
                except KeyError as e:
                    print(f"KeyError for product {i} on page {page}: {e}")

            page += 1
            if page > end_page:
                print(f'Total rows = {len(data_final)}')
                break
            else:
                data = self.send_request(page)

        df = pd.DataFrame(data_final, columns=['title', 'product_url', 'category', 'image_url', 'rating', 'price'])
        return df

    def save_json(self, filename='data.json'):
        """
        Save the first page of results to a JSON file.
        """
        result = self.send_request(1)
        with open(filename, 'w', encoding='utf8') as json_file:
            json.dump(result, json_file, ensure_ascii=False)
        print(f'Data stored in JSON file {filename} successfully.')

    def save_csv(self, filename='file_csv.csv'):
        """
        Save all scraped data to a CSV file.
        """
        df = self.get_data()
        df.to_csv(filename, sep=',', encoding='utf-8', index=False)
        print(f'Data stored in CSV file {filename} successfully.')

    @classmethod
    def start(cls, search, items):
        return cls(search, items)

    # ------------------ Proxy Methods ------------------

    def proxy(self):
        """
        Load proxy list from file and check availability.
        """
        proxy_list = []
        proxy_list_path = 'proxy_list.txt'
        try:
            with open(proxy_list_path, encoding='utf-8') as p:
                for row in p:
                    proxy_list.append(row.strip())
        except FileNotFoundError:
            print(f"Proxy list file not found: {proxy_list_path}")
            return

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.proxy_check_request, proxy_list)
            executor.shutdown(wait=True)
            self.proxy_selection()

    def proxy_selection(self):
        """
        Print available proxies.
        """
        print(f'Available proxies: {self.proxy_available}')

    def proxy_check_request(self, proxy):
        """
        Check if a proxy is working.
        """
        try:
            check = requests.get('https://www.google.com', proxies={'http': proxy, 'https': proxy}, timeout=3)
            if check.ok:
                print(f'Proxy {proxy} is available.')
                self.proxy_available.append(proxy)
        except requests.RequestException as e:
            print(f'Proxy {proxy} failed: {e}')
