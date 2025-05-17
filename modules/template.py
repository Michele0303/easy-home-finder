class Template:

    def __init__(self, url: str):
        self.url = url
        self.headers = {}
        self.extract_links_regex = ()
        self.tree = None

    def extract_links(self) -> list:
        raise NotImplementedError

    def get_title(self) -> str:
        raise NotImplementedError

    def get_price(self) -> str:
        raise NotImplementedError

    def get_listing_info(self, url: str) -> tuple[str, str]:
        raise NotImplementedError
