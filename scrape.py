import requests
import json
import re
from bs4 import BeautifulSoup


domain = "https://quotes.toscrape.com"
start_url = "/page/1/"
quotes_lst = []
authors = []
authors_rdy = []


def parse_cards(link):
    soup = BeautifulSoup(link.text, "lxml")
    quotes = soup.find_all("div", class_="quote")
    for quote_card in quotes:
        quote = quote_card.find("span", class_="text")
        author = quote_card.find("small", class_="author")
        tags_lst = quote_card.find_all("a", class_="tag")
        tags = []
        for tag in tags_lst:
            tags.append(tag.text)
        quote_dict = {"tags": tags, "author": author.text, "quote": quote.text}
        quotes_lst.append(quote_dict)
        if author.text not in authors_rdy:
            link = quote_card.find("a")
            parse_author(f"{domain}{link['href']}")


def parse_author(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "lxml")
    name = soup.find("h3", class_="author-title")
    born_date = soup.find("span", class_="author-born-date")
    born_loc = soup.find("span", class_="author-born-location")
    description = soup.find("div", class_="author-description")
    description = description.text.strip()
    pos = re.search("(More: http)", description)
    if pos:
        author = {"fullname": name.text, "born_date": born_date.text, "born_location": born_loc.text,
                  "description": description[:pos.span()[0]]}
    else:
        author = {"fullname": name.text, "born_date": born_date.text, "born_location": born_loc.text,
                  "description": description}
    authors_rdy.append(name.text)
    authors.append(author)


def fill_files():
    with open("authors.json", "w") as ph:
        json.dump(authors, ph, indent=True)

    with open("quotes.json", "w") as fp:
        json.dump(quotes_lst, fp, indent=True)


def main():
    for page in range(10):
        response = requests.get(f"{domain}/page/{page+1}/")
        parse_cards(response)
    fill_files()


if __name__ == "__main__":
    main()
