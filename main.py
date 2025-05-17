import argparse

from listing_monitoring import ListingMonitor
from modules.idealista_fetcher import IdealistaFetcher
from modules.immobiliare_fetcher import ImmobiliareFetcher
from modules.subito_fetcher import SubitoFetcher


def parse_args():
    """ Parse command line arguments. """
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", nargs='+',
                        help="List of URLs to monitor (separated by space)")
    parser.add_argument('--token', dest='token',
                        help="telegram bot token API")
    parser.add_argument('--chatid', dest='chatid',
                        help="telegram chatid where to receive messages")
    return parser.parse_args()

def get_fetcher(url):
    if "subito.it" in url:
        return SubitoFetcher(url)
    elif "idealista.it" in url:
        return IdealistaFetcher(url)
    elif "immobiliare.it" in url:
        return ImmobiliareFetcher(url)
    else:
        raise ValueError("Unsupported site")

if __name__ == '__main__':

    """
    parse = parse_args()
    if not parse.urls:
        print("Please provide at least one URL.")
        exit(1)
    if not parse.token:
        print("Please enter a telegram token")
        exit(1)
    if not parse.chatid:
        print("Please enter a telegram chatid")
        exit(1)

    urls = parse.urls
    token = parse.token
    chat_id = parse.chatid
    """

    urls = [
        #"https://www.subito.it/annunci-sardegna/vendita/appartamenti/cagliari/",
        "https://www.idealista.it/affitto-case/cagliari-cagliari/?ordine=pubblicazione-desc"
    ]
    token = "7846772183:AAGoGz7ENtjxXoNimulWxQpu2xNiqqoXHiA"
    chat_id = 1110107842

    bots = [
        ListingMonitor(
            fetcher=get_fetcher(url),
            token_api=token,
            chat_id=chat_id
        )
        for url in urls
    ]

    while True:
        for bot in bots:
            bot.check_for_updates()
