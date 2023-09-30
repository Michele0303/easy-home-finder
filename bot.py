import re

import requests as req


''''

PROVARE CON BURP A TROVARE SECRET API DI SUBITO.IT SFRUTTAND ANCHE L'ID 
FINALE IN OGNI LINK.


'''

class Bot:
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
            # first start
            self.queue = self.__extracts_links()

            # start monitoring
            while True:
                # extracts links from page
                tmp_links = self.__extracts_links()

                for x in tmp_links:
                    print(x)

                return

                for link in tmp_links:
                    # check if the extracted links are not already in the queue
                    if link not in self.queue:
                        self.__add_listing(link)
                        self.__send_notify(link)
        except Exception as ex:
            print(ex)
            pass

    def __extracts_links(self) -> list:
        content = req.get(self.url).text
        return re.findall(Bot.EXTRACT_LINKS_REGEX, content)

    def __add_listing(self, listing: str) -> None:
        if self.__is_queue_full():
            self.queue.pop(0)  # remove first element FIFO
        self.queue.append(listing)

    def __get_title(self) -> str:
        return self.url

    def __send_notify(self, link: str) -> None:
        pass

    def __is_queue_full(self) -> bool:
        return len(self.queue) == self.QUEUE_MAX_LEN
