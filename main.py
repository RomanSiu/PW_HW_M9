from scrape import main
from seeds import authors_handle, quotes_handle


def handle():
    main()
    authors_handle()
    quotes_handle()


if __name__ == '__main__':
    handle()
