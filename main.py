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

    parse = parse_args()
    if not parse.url:
        print("Please enter a url")
        exit(1)
    if not parse.token:
        print("Please enter a telegram token")
        exit(1)
    if not parse.chatid:
        print("Please enter a telegram chatid")
        exit(1)

    url = parse.url
    token = parse.token
    chat_id = parse.chatid

    subito_bot = Bot(
        url=url,
        token_api=token,
        chat_id=chat_id,
    )

    subito_bot.start_monitoring()
