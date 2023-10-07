import re

import requests as req

from lxml import html


class Bot:
    # Regular expression for extracting links from the page
    EXTRACT_LINKS_REGEX = ("<div class=\"items__item item-card item-card--big "
                           "BigCard-module_card__Exzqv\"><a href=\"(.*?)\"")

    def __init__(self, url: str, token_api: str, chat_id: int):
        # subito.it settings
        self.url = url
        self.delay = 1  # 1 minute

        # queue
        self.queue = []
        self.QUEUE_MAX_LEN = 30

        # telegram settings
        self.token_api = token_api
        self.chat_id = chat_id

    def start_monitoring(self):
        try:
            # Initial extraction of links
            self.queue = self.__extracts_links()

            # Start monitoring loop
            while True:
                # Extract links from the page
                tmp_links = self.__extracts_links()

                for link in tmp_links:
                    # Check if the extracted links are not already in the queue
                    if link not in self.queue:
                        self.__add_listing(link)
                        self.__send_notify(link)

        except Exception as ex:
            print(ex)
            pass

    def __extracts_links(self) -> list:
        """ Return all listings on the page. """
        try:
            content = req.get(self.url).text
            return re.findall(Bot.EXTRACT_LINKS_REGEX, content)
        except Exception:
            return []

    def __add_listing(self, listing: str) -> None:
        """ Adds the listing to the queue. """
        if self.__is_queue_full():
            self.queue.pop(0)  # remove first element FIFO
        self.queue.append(listing)

    def __get_listing_info(self, url: str):
        """" Return listing information.  """
        try:
            content = req.get(url).text
            self.tree = html.fromstring(content)

            title = self.__get_title()
            price = self.__get_price()

            return title, price
        except Exception:
            pass

    def __get_title(self) -> str:
        """ Return the title of the listing. """
        try:
            return self.tree.xpath('//*[@id="layout"]/main/div[3]/div['
                                   '1]/div[1]/section/div[2]/h1/text()')[0]
        except Exception:
            return ""

    def __get_price(self) -> str:
        """ Return the price of the listing. """
        try:
            return self.tree.xpath('//*[@id="layout"]/main/div[3]/div['
                                   '1]/div[1]/section/div[2]/p/text()')[0]
        except Exception:
            return ""

    def __send_notify(self, url: str) -> None:
        """ Send notify to telegram """
        try:
            title, price = self.__get_listing_info(url)

            message = (f"🚨 <b>Nuovo Annuncio</b> 🚨\n\n"
                       f"<b>Titolo:</b> <code>{title}</code>\n\n"
                       f"<b>Prezzo:</b> <i>{price}</i>\n\n"
                       f"<b>Url:</b> <a href='{url}'>vai all'annuncio</a>")

            api_url = (f"https://api.telegram.org/bot"
                       f"{self.token_api}/sendMessage"
                       f"?chat_id={self.chat_id}"
                       f"&text={message}"
                       f"&parse_mode=html")

            req.get(api_url)
        except Exception:
            pass

    def __is_queue_full(self) -> bool:
        """ Check if queue is full. """
        return len(self.queue) == self.QUEUE_MAX_LEN
