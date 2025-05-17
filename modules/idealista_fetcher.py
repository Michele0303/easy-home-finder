import re

import requests
from lxml import html

from modules.listing_fetcher import ListingFetcher


class IdealistaFetcher(ListingFetcher):

    def __init__(self, url: str):
        self.url = url
        self.headers = {
            "Cache-Control": "max-age=0",
            "Sec-Ch-Ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Linux\"", "Dnt": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "it-IT,it;q=0.9,en-IT;q=0.8,en;q=0.7,en-US;q=0.6",
            "Priority": "u=0, i", "Connection": "keep-alive"
        }
        self.extract_links_regex = '<a href="(.*?)" role="heading"'
        self.tree = None

    def extract_links(self) -> list:
        content = requests.get(self.url, headers=self.headers).text
        links = re.findall(self.extract_links_regex, content)
        return ['https://www.idealista.it' + link for link in links]

    def get_title(self) -> str:
        """ Return the title of the listing. """
        try:
            return self.tree.xpath('//*[@id="main"]/div/main/section[2]/section/div[1]/h1/span/text()')[0]
        except Exception:
            raise

    def get_price(self) -> str:
        """ Return the price of the listing. """
        try:
            return self.tree.xpath('//*[@id="main"]/div/main/section[2]/section/div[2]/span/span/text()')[0] + ' €'
        except Exception:
            raise

    def get_listing_info(self, url: str) -> tuple[str, str] | None:
        try:
            content = requests.get(url, headers=self.headers).text
            self.tree = html.fromstring(content)

            title = self.get_title()
            price = self.get_price()

            return title, price
        except Exception as ex:
            print('Error during extracting listing info:', ex)

