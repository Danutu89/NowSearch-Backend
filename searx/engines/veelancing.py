from collections.abc import Iterable
from json import loads, dumps
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
    "jobs",
    "job",
]
from searx import logger

logger = logger.getChild("search")


def request(query, params):
    query = urlencode({"q": query})[2:]
    parsed_query = query
    matches = [x for x in keywords if x in query.lower()]

    if len(matches) > 0:
        parsed_query = query.replace(matches[0], "")

    params["method"] = "POST"
    params["url"] = search_url
    params["data"]["filters"] = {"name": parsed_query}
    logger.info(params)
    return params


def response(resp):
    results = []
    json = loads(resp.text)

    for res in json["results"]:
        temp = res
        temp["content"] = res["description"]
        temp["job_category"] = res["category"]
        temp["url"] = "https://veelancing.io{}".format(temp["link"])
        del temp["description"]
        del temp["category"]
        results.append(temp)

    return results