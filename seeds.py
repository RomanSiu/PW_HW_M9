from models import Author, Quote
from datetime import datetime
import json
import connect


def authors_handle():
    with open("authors.json", "r") as fh:
        authors = json.load(fh)

    for a in authors:
        date = datetime.strptime(a["born_date"], "%B %d, %Y")
        Author(fullname=a["fullname"], born_date=date, born_location=a["born_location"],
               description=a["description"]).save()


def quotes_handle():
    with open("quotes.json", "r") as fh:
        quotes = json.load(fh)

    for q in quotes:
        author_ref = Author.objects(fullname=q["author"])
        Quote(tags=q["tags"], author=author_ref[0], quote=q["quote"]).save()


if __name__ == "__main__":
    authors_handle()
    quotes_handle()
