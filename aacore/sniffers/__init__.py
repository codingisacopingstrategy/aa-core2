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


sniffers = []


rdfa = RDF.Parser("rdfa")
tidy = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("lxml"), namespaceHTMLElements=False)


def extract(d, keys):
    return dict((k, d[k]) for k in keys if k in d)


def sniffer(mime_pattern):
    def decorator(cls):
        sniffers.append(cls)
        return cls
    return decorator 


class AAResource(object):
    def __init__(self, url):
        self.url = url
        self.dummy_model = self.get_dummy_model()

    def get_sniffers(self, mime):
        cls = []
        for sniffer in sniffers:
            #if getattr(sniffer, "test"):
            if sniffer().test(self.dummy_model):
                cls.append(sniffer)
        return cls

    def get_dummy_model(self):
        """
        Creates and returns an in-memory HashStorage RDF Model.

        It is useful for testing purpose or for temporary storage.
        """
        options = "new='yes', hash-type='memory', contexts='yes'"
        storage = RDF.HashStorage('dummy', options=options)
        return RDF.Model(storage)

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

        #import pdb; pdb.set_trace() 
        #foo = rdfa.parse_string_as_stream(t.render(c).encode("utf-8"), self.url)
        rdfa.parse_string_into_model(self.dummy_model, t.render(c).encode("utf-8"), self.url)

        rdfa.parse_string_into_model(RDF_MODEL, t.render(c).encode("utf-8"), self.url)
        RDF_MODEL.sync()

        mime = magic.from_buffer(data.file.read(1024), mime=True)
        print(mime)
        for sniffer in self.get_sniffers(mime):
            print(sniffer)
        #if sniffer:
            #html = sniffer().sniff(self.url)
            #rdfa.parse_string_into_model(RDF_MODEL, html.encode("utf-8"), self.url)
            #RDF_MODEL.sync()


map(__import__, SNIFFERS)
