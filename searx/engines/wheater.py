from collections.abc import Iterable
from json import loads
from urllib.parse import urlencode
from searx.utils import to_string


search_url = None

# parameters for engines with paging support
#
# number of results on each page
# (only needed if the site requires not a page number, but an offset)
page_size = 1
# number of the first page (usually 0 or 1)
first_page_num = 0

keywords = [
    "meteo",
    "weather",
    "weather in",
    "meteo in",
]


def request(query, params):
    query = urlencode({"q": query})[2:]

    matches = [x for x in keywords if x in query.lower()]

    if len(matches) == 0:
        return params

    fp = {"query": query.replace(matches[0], "")}
    params["url"] = search_url.format(**fp)
    params["query"] = query

    return params


def response(resp):
    results = []
    json = loads(resp.text)

    results.append({"answer": "weather", "data": json, "url": search_url})
    return results
