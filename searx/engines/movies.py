from collections.abc import Iterable
from json import loads
from urllib.parse import urlencode
from searx.utils import to_string

# parameters for engines with paging support
#
# number of results on each page
# (only needed if the site requires not a page number, but an offset)
page_size = 1
# number of the first page (usually 0 or 1)
first_page_num = 0

keywords = [
    "movie",
    "movies",
    "weather in",
    "meteo in",
]

base_url = "https://api.themoviedb.org/3"


def request(query, params):
    query = urlencode({"q": query})[2:]
    parsed_query = query

    matches = [x for x in keywords if x in query]

    if len(matches) > 0:
        parsed_query = query.replace(matches[0], "")

    params["url"] = (
        base_url
        + f"/search/movie?query={parsed_query}&api_key=ae96477b92962a9d3a46489b29affd03"
    )
    params["query"] = query

    return params


def response(resp):
    results = []
    json = loads(resp.text)

    if "results" in json and len(json["results"]) > 1:
        results.append({"infobox": json["results"][0], "url": base_url})
        results.append({"movies": json["results"], "url": base_url})
    return results
