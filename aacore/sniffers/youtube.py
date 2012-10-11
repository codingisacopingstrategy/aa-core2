from aacore.sniffers import sniffer


@sniffer("text/html")
class YoutubeSniffer(object):
    def sniff(self, url):
        print("sniffed an youtube page")
        print(url)
        return "ok"
