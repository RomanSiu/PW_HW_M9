import redis
from models import Author, Quote
from redis_lru import RedisLRU
import connect


def input_error(func):
    def inner(*args):
        try:
            result = func(*args)
        except IndexError:
            print("There is no such record!")
            main()
        else:
            return result
    return inner


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@input_error
def main():
    while True:
        inp_arg = inp()
        if inp_arg == "exit":
            break
        args = inp_arg.split(":")
        if args[0] == "name":
            res = author_search(args[1])
            cl_output(res)
        elif args[0] in ["tags", "tag"]:
            res = tags_search(args[1])
            cl_output(res)
        else:
            print("Invalid command!")


@cache
def author_search(arg):
    author_ref = Author.objects(fullname__istartswith=arg)
    quotes_lst = []
    for author in author_ref:
        quotes = Quote.objects(author=author)
        quotes_lst.extend(quotes)
    return quotes_lst


@cache
def tags_search(args):
    args_lst = args.split(",")
    quotes = []
    for i in args_lst:
        quote = Quote.objects(tags__icontains=i)
        for q in quote:
            if q not in quotes:
                quotes.append(q)
    return quotes


def inp():
    arg = input(">>>")
    return arg


def cl_output(res):
    for i in res:
        print(f"Author: {i.author.fullname}, Tags: {i.tags}, Quote: {i.quote}")


if __name__ == '__main__':
    main()
