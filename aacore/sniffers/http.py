import magic
import requests

from aacore.sniffers import sniffer
from django.template import Context
from django.template.loader import get_template


@sniffer("rdfa")
class HttpSniffer(object):
    def __init__(self, request=None, model=None):
        self.request = request
        self.model = model

    def test(self):
        return True

    def sniff(self):
        print("sniffed an http resource")

        # Detects the mime type from content as an alternative to content-type
        # We make a new request to avoid consuming self.request response body
        # FIXME: there should be a way to avoid doing a second request.
        #        See <http://stackoverflow.com/questions/13197854/>
        request = requests.get(self.request.url, prefetch=False)
        mime = magic.from_buffer(request.iter_content(1024).next(), mime=True)

        # Maps the HTTP metadata to RDFa and indexes it in a temporary model
        t = get_template("aacore/http.html")
        c = Context({'headers': dict(**self.request.headers), 'mime': mime, 'url': self.request.url})

        return t.render(c).encode("utf-8")

