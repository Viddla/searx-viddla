# SPDX-License-Identifier: AGPL-3.0-or-later
"""
 Viddla (Videos)
"""

from json import loads
from datetime import datetime
from urllib.parse import urlencode
from searx.utils import match_language, html_to_text

# about
about = {
    "website": 'https://vidd.la',
    "wikidata_id": None,
    "official_api_documentation": 'https://docs.vidd.la/',
    "use_official_api": True,
    "require_api_key": False,
    "results": 'JSON',
}

# engine dependent config
categories = ['videos']
paging = True
time_range_support = True

# search-url
search_url = 'https://api-dev.vidd.la/search?fields=date,title,shdesc,longdesc,duration,url,thumbnail,id&sort=relevance&limit=5&page={pageno}&{query}'  # noqa
embedded_url = '<iframe frameborder="0" width="540" height="304" ' +\
    'data-src="https://embed.vidd.la/{videoid}" allowfullscreen></iframe>'

# do search-request
def request(query, params):

    params['url'] = search_url.format(
        query=urlencode({'search': query}),
        pageno=params['pageno'])

    return params


# get response from search-request
def response(resp):
    results = []

    search_res = loads(resp.text)

    # return empty array if there are no results
    if 'list' not in search_res:
        return []

    # parse results
    for res in search_res['list']:
        title = res['title']
        url = res['url']
        content = html_to_text(res['description'])
        thumbnail = res['thumbnail_360_url']
        publishedDate = datetime.fromtimestamp(res['created_time'], None)
        embedded = embedded_url.format(videoid=res['id'])

        # http to https
        thumbnail = thumbnail.replace("http://", "https://")

        results.append({'template': 'videos.html',
                        'url': url,
                        'title': title,
                        'content': content,
                        'publishedDate': publishedDate,
                        'embedded': embedded,
                        'thumbnail': thumbnail})

    # return results
    return results
