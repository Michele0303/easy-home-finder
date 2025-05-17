import requests
import re
from lxml import html

from modules.listing_fetcher import ListingFetcher


class SubitoFetcher(ListingFetcher):

    def __init__(self, url: str):
        self.url = url
        self.headers = {
            "Sec-Ch-Ua": '"Not:A-Brand";v="24", "Chromium";v="134"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Linux\"",
            "Accept-Language": "en-US,en;q=0.9",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=0, i",
        }
        self.extract_links_regex = (
            "<div class=\"items__item item-card item-card--big "
            "BigCard-module_card__Exzqv\"><a href=\"(.*?)\""
        )
        self.tree = None

    def extract_links(self) -> list:
        content = requests.get(self.url, headers=self.headers).text
        return re.findall(self.extract_links_regex, content)

    def get_title(self) -> str:
        """ Return the title of the listing. """
        try:
            return self.tree.xpath('//*[@id="layout"]/main/div[2]/div/div[3]/div[1]/div[1]/section/div[2]/h1/text()')[0]
        except Exception:
            raise

    def get_price(self) -> str:
        """ Return the price of the listing. """
        try:
            return self.tree.xpath('//*[@id="layout"]/main/div[2]/div/div[3]/div[1]/div[1]/section/div[2]/div[3]/div/p/text()')[0]
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
