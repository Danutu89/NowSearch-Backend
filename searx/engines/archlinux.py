# -*- coding: utf-8 -*-

"""
 Arch Linux Wiki

 @website      https://wiki.archlinux.org
 @provide-api  no (Mediawiki provides API, but Arch Wiki blocks access to it
 @using-api    no
 @results      HTML
 @stable       no (HTML can change)
 @parse        url, title
"""

from urllib.parse import urlencode, urljoin
from lxml import html
from searx.utils import extract_text, eval_xpath_list, eval_xpath_getindex

# engine dependent config
categories = ["it"]
language_support = True
paging = True
base_url = "https://wiki.archlinux.org"

# xpath queries
xpath_results = '//ul[@class="mw-search-results"]/li'
xpath_link = './/div[@class="mw-search-result-heading"]/a'


# cut 'en' from 'en-US', 'de' from 'de-CH', and so on
def locale_to_lang_code(locale):
    if locale.find("-") >= 0:
        locale = locale.split("-")[0]
    return locale


# wikis for some languages were moved off from the main site, we need to make
# requests to correct URLs to be able to get results in those languages
lang_urls = {
    "all": {
        "base": "https://wiki.archlinux.org",
        "search": "/index.php?title=Special:Search&offset={offset}&{query}",
    },
    "de": {
        "base": "https://wiki.archlinux.de",
        "search": "/index.php?title=Spezial:Suche&offset={offset}&{query}",
    },
    "fr": {
        "base": "https://wiki.archlinux.fr",
        "search": "/index.php?title=Spécial:Recherche&offset={offset}&{query}",
    },
    "ja": {
        "base": "https://wiki.archlinuxjp.org",
        "search": "/index.php?title=特別:検索&offset={offset}&{query}",
    },
    "ro": {
        "base": "http://wiki.archlinux.ro",
        "search": "/index.php?title=Special:Căutare&offset={offset}&{query}",
    },
    "tr": {
        "base": "http://archtr.org/wiki",
        "search": "/index.php?title=Özel:Ara&offset={offset}&{query}",
    },
}


# get base & search URLs for selected language


# Language names to build search requests for
# those languages which are hosted on the main site.
main_langs = {
    "ar": "العربية",
    "bg": "Български",
    "cs": "Česky",
    "da": "Dansk",
    "el": "Ελληνικά",
    "es": "Español",
    "he": "עברית",
    "hr": "Hrvatski",
    "hu": "Magyar",
    "it": "Italiano",
    "ko": "한국어",
    "lt": "Lietuviškai",
    "nl": "Nederlands",
    "pl": "Polski",
    "pt": "Português",
    "ru": "Русский",
    "sl": "Slovenský",
    "th": "ไทย",
    "uk": "Українська",
    "zh": "简体中文",
}
supported_languages = dict(lang_urls, **main_langs)


# do search-request
def request(query, params):
    # prepare the request parameters
    query = urlencode({"search": query})
    offset = (params["pageno"] - 1) * 20

    # get request URLs for our language of choice
    urls = lang_urls["all"]
    search_url = urls["base"] + urls["search"]

    params["url"] = search_url.format(query=query, offset=offset)

    return params


# get response from search-request
def response(resp):
    # get the base URL for the language in which request was made
    base_url = lang_urls["all"]["base"]

    results = []

    dom = html.fromstring(resp.text)

    # parse results
    for result in eval_xpath_list(dom, xpath_results):
        link = eval_xpath_getindex(result, xpath_link, 0)
        href = urljoin(base_url, link.attrib.get("href"))
        title = extract_text(link)

        results.append({"url": href, "title": title})

    return results
