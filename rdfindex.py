import urllib2
import magic
import re
import subprocess
import RDF
import html5lib
from django.template import Template, Context
from django.conf import settings
from urllib2utils import ResourceOpener


if __name__ == "__main__":
    settings.configure()


sniffers = {}


storage_dir = "/tmp"
storage_name = "aa"

options = "hash-type='bdb', contexts='yes', dir='%s'" % storage_dir
storage = RDF.HashStorage(storage_name, options=options)
model = RDF.Model(storage)

rdfa = RDF.Parser("rdfa")
tidy = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("lxml"), namespaceHTMLElements=False)


def extract(d, keys):
    return dict((k, d[k]) for k in keys if k in d)


def sniffer(mime_pattern):
    def decorator(cls):
        sniffers[mime_pattern] = cls
        return cls
    return decorator 


@sniffer("image/*")
class ImageSniffer(object):
    def sniff(self, url):
        print("sniffed an image")
        print(url)


@sniffer("text/html")
class YoutubeSniffer(object):
    def sniff(self, url):
        print("sniffed an youtube page")
        print(url)


@sniffer("text/html")
class HtmlSniffer(object):
    def sniff(self, url):
        print("sniffed an html page")
        print(url)


@sniffer("application/ogg")
class OggSniffer(object):
    def sniff(self, url):
        print("sniffed an ogg file")
        print(url)
        cmd = ['ffprobe', '-show_format', '-show_streams', '-pretty', '-loglevel', 'quiet', url]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err =  p.communicate()
        print(out)


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

        t = Template("""<?xml version="1.0" encoding="UTF-8"?>
            <html xmlns="http://www.w3.org/1999/xhtml" 
                xmlns:aa="http://activearchives.org/terms/"
                version="XHTML+RDFa 1.1"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="http://www.w3.org/1999/xhtml
                                    http://www.w3.org/MarkUp/SCHEMA/xhtml-rdfa-2.xsd"
                lang="en"
                xml:lang="en">
              <head>
                <title>Virtual Library</title>
              </head>
              <body>
                    <p about="{{ url }}">
                    <span property="aa:content-type">{{ metadata.content_type }}</span>
                    <span property="aa:charset">{{ metadata.charset }}</span>
                    <span property="aa:last_modified">{{ metadata.last_modified }}</span>
                    </p>
              </body>
            </html>""")

        c = Context({'metadata': metadata, 'url': self.url})

        rdfa.parse_string_into_model(model, t.render(c).encode("utf-8"), self.url)
        model.sync()

        mime = magic.from_buffer(data.file.read(1024), mime=True)
        print(mime)
        sniffer = self.get_sniffer(mime)
        if sniffer:
            sniffer().sniff(self.url)


if __name__ == "__main__":
    AAResource("http://stdin.fr").index()
    AAResource("http://video.constantvzw.org/AAworkshop/saturdaytimelapse.avi").index()
    AAResource("http://video.constantvzw.org/AAworkshop/MVI_1673.ogv").index()
    AAResource("http://upload.wikimedia.org/wikipedia/commons/1/1d/ARS-habanero.jpg").index()
    AAResource("http://horsefactor.free.fr/?feed=rss2").index()
