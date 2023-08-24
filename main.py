urls = []


def load_links():
    with open('urls.txt', 'r') as file:
        for line in file:
            urls.append(line.strip())


def main() -> None:
    pass


if __name__ == '__main__':
    main()
