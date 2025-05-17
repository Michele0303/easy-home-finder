from modules.listing_fetcher import ListingFetcher


class ImmobiliareFetcher(ListingFetcher):

    def __init__(self, url: str):
        self.url = url
        self.extract_links_regex = ''
        self.headers = {}

    def extract_links(self) -> list:
        raise NotImplementedError

    def get_listing_info(self, url: str) -> tuple[str, str]:
        raise NotImplementedError

