from aacore.sniffers import sniffer


@sniffer("image/*")
class ImageSniffer(object):
    def sniff(self, url):
        print("sniffed an image")
        print(url)
        return "ok"
