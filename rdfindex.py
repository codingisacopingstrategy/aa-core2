import urllib2
import magic
import re
import subprocess


sniffers = {}


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
        print("sniffed an html page")
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
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open(self.url)

        print(response.info())

        mime = magic.from_buffer(response.read(1024), mime=True)
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
