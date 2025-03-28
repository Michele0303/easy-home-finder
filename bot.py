import re
import time
import requests as req
from lxml import html


class Bot:
    EXTRACT_LINKS_REGEX = (
        "<div class=\"items__item item-card item-card--big "
        "BigCard-module_card__Exzqv\"><a href=\"(.*?)\""
    )

    HEADERS = {
        "Sec-Ch-Ua": "\"Chromium\";v=\"129\", \"Not=A?Brand\";v=\"8\"",
        "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Linux\"",
        "Accept-Language": "en-US,en;q=0.9",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i",
        "Connection": "keep-alive"
    }

    def __init__(self, url: str, token_api: str, chat_id: int):
        self.url = url
        self.delay = 60  # seconds
        self.queue = []
        self.QUEUE_MAX_LEN = 90
        self.token_api = token_api
        self.chat_id = chat_id
        self.queue = self.__extract_links()

    def check_for_updates(self):
        """Checks for new listings and sends a notification if found."""
        try:
            new_links = self.__extract_links()
            for link in new_links:
                if link not in self.queue:
                    self.__add_to_queue(link)
                    self.__send_notification(link)
            time.sleep(self.delay)
        except Exception as ex:
            print(f"[{self.url}] Error: {ex}")

    def __extract_links(self) -> list:
        try:
            content = req.get(self.url, headers=Bot.HEADERS).text
            return re.findall(Bot.EXTRACT_LINKS_REGEX, content)
        except Exception as ex:
            print('Error during extracting links:', ex)
            return []

    def __add_to_queue(self, listing: str) -> None:
        if len(self.queue) >= self.QUEUE_MAX_LEN:
            self.queue.pop(0)
        self.queue.append(listing)

    def __get_listing_info(self, url: str):
        """" Return listing information.  """
        try:
            content = req.get(url, headers=Bot.HEADERS).text
            self.tree = html.fromstring(content)

            title = self.__get_title()
            price = self.__get_price()

            return title, price
        except Exception:
            raise

    def __get_title(self) -> str:
        """ Return the title of the listing. """
        try:
            return self.tree.xpath('//*[@id="layout"]/main/div[2]/div/div[3]/div[1]/div[1]/section/div[2]/h1/text()')[0]
        except Exception:
            raise

    def __get_price(self) -> str:
        """ Return the price of the listing. """
        try:
            return self.tree.xpath('//*[@id="layout"]/main/div[2]/div/div[3]/div[1]/div[1]/section/div[2]/div[3]/div/p/text()')[0]
        except Exception:
            raise

    def __send_notification(self, url: str) -> None:
        try:
            title, price = self.__get_listing_info(url)
            message = (
                f"🚨 <b>New Listing</b> 🚨\n\n"
                f"<b>Title:</b> <code>{title}</code>\n\n"
                f"<b>Price:</b> <i>{price}</i>\n\n"
                f"<b>URL:</b> <a href='{url}'>View listing</a>"
            )

            api_url = (
                f"https://api.telegram.org/bot{self.token_api}/sendMessage"
                f"?chat_id={self.chat_id}"
                f"&text={message}"
                f"&parse_mode=html"
            )
            req.get(api_url)
        except Exception as ex:
            print('Error during sending notification:', ex)
