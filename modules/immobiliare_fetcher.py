import requests
import re
from lxml import html

from modules.listing_fetcher import ListingFetcher


class ImmobiliareFetcher(ListingFetcher):

    def __init__(self, url: str):
        self.url = url
        self.extract_links_regex = ''
        self.headers = {}

    def extract_links(self) -> list:
        content = requests.get(self.url, headers=self.headers).text
        return re.findall(self.extract_links_regex, content)

    def get_listing_info(self, url: str) -> tuple[str, str]:
        content = requests.get(url, headers=self.headers).text
        tree = html.fromstring(content)
        title = tree.xpath('...')[0]
        price = tree.xpath('...')[0]
        return title, price
