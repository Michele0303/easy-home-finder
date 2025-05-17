import time

import requests

from modules.listing_fetcher import ListingFetcher

class ListingMonitor:
    def __init__(self, fetcher: ListingFetcher, token_api: str, chat_id: int):
        self.fetcher = fetcher
        self.queue = []

        self.token_api = token_api
        self.chat_id = chat_id

        self.delay = 60 # seconds

    def check_for_updates(self):
        try:
            new_links = self.fetcher.extract_links()
            for link in new_links:
                if link not in self.queue:
                    self.__send_notification(link)
                    self.__add_to_queue(link)
            time.sleep(self.delay)
        except Exception as ex:
            print(f"Error: {ex}")

    def __add_to_queue(self, link):
        if len(self.queue) >= 120:
            self.queue.pop(0)
        self.queue.append(link)

    def __send_notification(self, url):
        try:
            title, price = self.fetcher.get_listing_info(url)

            message = (f"🚨 <b>Nuovo Annuncio</b> 🚨\n\n"
                       f"<b>Titolo:</b> <code>{title}</code>\n\n"
                       f"<b>Prezzo:</b> <i>{price}</i>\n\n"
                       f"<b>Url:</b> <a href='{url}'>vai all'annuncio</a>")

            api_url = (f"https://api.telegram.org/bot"
                       f"{self.token_api}/sendMessage"
                       f"?chat_id={self.chat_id}"
                       f"&text={message}"
                       f"&parse_mode=html")

            requests.get(api_url)
        except Exception as ex:
            print('Error during sending notification:', ex)
