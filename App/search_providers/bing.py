import re
import requests
from requests.exceptions import RequestException


class BingSearcher(object):

    @classmethod
    def images(cls, query):
        html = cls._fetch_html(query)
        urls = cls._url_matches(html)
        # app.logger.debug("Bing: Found %s URLs mathing query '%s'" % (len(urls), query))

        return urls

    @classmethod
    def _fetch_html(cls, query):
        payload = {
            'qft': '+filterui:photo-photo',
            'q': query
        }
        try:
            html = requests.get('http://www.bing.com/images/search', params=payload).text
        except RequestException:
            html = ''
            # app.logger.warning('Request failed while searching Bing images for %' % query)
        return html

    @classmethod
    def _url_matches(cls, html):
        img_url_matcher = re.compile('(<[^<]* m="{[^\"]*imgurl:&quot;([^\&]*)&quot;[^\"]*}")')
        matches = img_url_matcher.findall(html)

        return [m[1] for m in matches if cls._is_sfw(m)]

    @classmethod
    def _is_sfw(cls, match):
        return re.search('fz="1"', match[0]) is None
