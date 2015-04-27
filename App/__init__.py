from flask import Flask, redirect
from requests.exceptions import ConnectionError
from search_providers.bing import BingSearcher
import requests
app = Flask(__name__)


@app.route("/")
def welcome():
    return "search-query.jpg.sexy"


@app.route("/", subdomain="<query>")
@app.route("/<query>")
def redirect_to_image(query):
    app.logger.debug("Looking for an image matching '%s'" % query)
    for url in BingSearcher.images(query):
        if is_live_url(url):
            app.logger.debug("Redirecting to '%s'" % url)
            return redirect(url)
    app.logger.debug("No images found :(")
    return "No results"


def is_live_url(url):
    app.logger.debug("Testing validity of URL '%s'" % url)
    try:
        r = requests.request('HEAD', url, allow_redirects=True)
        is_live = r.status_code in [301, 302, 200]
    except ConnectionError:
        app.logger.debug("URL '%s' is dead. ConnectionError" % url)
        return False

    if is_live:
        app.logger.debug("URL '%s' is live with status code %s" % (url, r.status_code))
        return True
    else:
        app.logger.debug("URL '%s' is dead with status code %s" % (url, r.status_code))
        return False

if __name__ == "__main__":
    app.run(debug=True)
