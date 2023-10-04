import argparse


def parse_args():
    """ Parse command line arguments. """
    parser = argparse.ArgumentParser()
    parser.add_argument("--url",
                        help="url of the page to be monitored")
    parser.add_argument('--token', dest='token',
                        help="telegram bot token API")
    parser.add_argument('--chatid', dest='chatid',
                        help="telegram chatid where to receive messages")
    return parser.parse_args()


if __name__ == '__main__':

    from bot import Bot

    url = ("https://www.subito.it/annunci-sardegna/affitto/camere-posti-letto"
           "/cagliari/cagliari/")

    subito_bot = Bot(
        url,
        "5217482235:AAGtYQCxN3swOWn-IeVfA-JZi7vD-H1LKK4",
        955112744,
    )
    subito_bot.start_monitoring()
