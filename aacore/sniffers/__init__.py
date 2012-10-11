import urllib2
import magic
import re
import subprocess
import RDF
import html5lib
from django.template import Template, Context
from urllib2utils import ResourceOpener

from aacore import RDF_MODEL
from aacore.settings import SNIFFERS
from django.template.loader import get_template


sniffers = {}


rdfa = RDF.Parser("rdfa")
tidy = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("lxml"), namespaceHTMLElements=False)


def extract(d, keys):
    return dict((k, d[k]) for k in keys if k in d)


def sniffer(mime_pattern):
    def decorator(cls):
        sniffers[mime_pattern] = cls
        return cls
    return decorator 


class AAResource(object):
    def __init__(self, url):
        self.url = url

    def get_sniffer(self, mime):
        for r in sniffers.keys():
            if re.match(r, mime) != None:
                return sniffers[r]

    def index(self):
        print("indexing %s" % self.url)

        try:
            data = ResourceOpener(url=self.url)
            data.get()
        except urllib2.HTTPError, e:
            data.status = e.code

        interesting_keys = ['content_type', 'charset', 'content_length', 'last_modified', 'etag', 'status']
        metadata = extract(data.__dict__, interesting_keys)
        print metadata

        t = get_template("aacore/http.html")
        c = Context({'metadata': metadata, 'url': self.url})

        rdfa.parse_string_into_model(RDF_MODEL, t.render(c).encode("utf-8"), self.url)
        RDF_MODEL.sync()

        mime = magic.from_buffer(data.file.read(1024), mime=True)
        print(mime)
        sniffer = self.get_sniffer(mime)
        if sniffer:
            html = sniffer().sniff(self.url)
            rdfa.parse_string_into_model(RDF_MODEL, html.encode("utf-8"), self.url)
            RDF_MODEL.sync()


map(__import__, SNIFFERS)
