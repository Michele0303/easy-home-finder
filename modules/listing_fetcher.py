class ListingFetcher:
    def extract_links(self) -> list:
        raise NotImplementedError

    def get_listing_info(self, url: str) -> tuple[str, str]:
        raise NotImplementedError
