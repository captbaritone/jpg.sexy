import re
import requests
from requests.exceptions import RequestException


class BingSearcher(object):

    @classmethod
    def images(cls, query):
        payload = {
            'qft': '+filterui:photo-photo',
            'q': query
        }
        try:
            html = requests.get('http://www.bing.com/images/search', params=payload).text
        except RequestException:
            # app.logger.warning('Request failed while searching Bing images for %' % query)
            return []

        urls = cls._url_matches(html)
        # Exclude matches including 'fz="1"'
        # app.logger.debug("Bing: Found %s URLs mathing query '%s'" % (len(urls), query))

        return urls

    @classmethod
    def _url_matches(cls, html):
        img_url_matcher = re.compile('( m="{[^\"]*imgurl:&quot;([^\&]*)&quot;[^\"]*}")')
        matches = img_url_matcher.findall(html)

        return [m[1] for m in matches]

    def _is_sfw(cls, match):
        return True
