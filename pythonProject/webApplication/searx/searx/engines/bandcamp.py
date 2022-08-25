"""
Bandcamp (Music)

@website     https://bandcamp.com/
@provide-api no
@results     HTML
@parse       url, title, content, publishedDate, embedded, thumbnail
"""

from urllib.parse import urlencode, urlparse, parse_qs
from dateutil.parser import parse as dateparse
from lxml import html
from searx.utils import extract_text

categories = ['music']
paging = True

base_url = "https://bandcamp.com/"
search_string = search_string = 'search?{query}&page={page}'
embedded_url = '''<iframe width="100%" height="166"
    scrolling="no" frameborder="no"
    data-src="https://bandcamp.com/EmbeddedPlayer/{type}={result_id}/size=large/bgcol=ffffff/linkcol=0687f5/tracklist=false/artwork=small/transparent=true/"
></iframe>'''


def request(query, params):
    '''pre-request callback
    params<dict>:
      method  : POST/GET
      headers : {}
      data    : {} # if method == POST
      url     : ''
      category: 'search category'
      pageno  : 1 # number of the requested page
    '''

    search_path = search_string.format(
        query=urlencode({'q': query}),
        page=params['pageno'])

    params['url'] = base_url + search_path

    return params


def response(resp):
    '''post-response callback
    resp: requests response object
    '''
    results = []
    tree = html.fromstring(resp.text)
    search_results = tree.xpath('//li[contains(@class, "searchresult")]')
    for result in search_results:
        link = result.xpath('.//div[@class="itemurl"]/a')[0]
        result_id = parse_qs(urlparse(link.get('href')).query)["search_item_id"][0]
        title = result.xpath('.//div[@class="heading"]/a/text()')
        date = dateparse(result.xpath('//div[@class="released"]/text()')[0].replace("released ", ""))
        content = result.xpath('.//div[@class="subhead"]/text()')
        new_result = {
            "url": extract_text(link),
            "title": extract_text(title),
            "content": extract_text(content),
            "publishedDate": date,
        }
        thumbnail = result.xpath('.//div[@class="art"]/img/@src')
        if thumbnail:
            new_result['thumbnail'] = thumbnail[0]
        if "album" in result.classes:
            new_result["embedded"] = embedded_url.format(type='album', result_id=result_id)
        elif "track" in result.classes:
            new_result["embedded"] = embedded_url.format(type='track', result_id=result_id)
        results.append(new_result)
    return results
