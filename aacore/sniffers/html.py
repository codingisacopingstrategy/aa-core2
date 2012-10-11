from sniffers import sniffer


@sniffer("text/html")
class HtmlSniffer(object):
    def sniff(self, url):
        print("sniffed an html page")
        print(url)
