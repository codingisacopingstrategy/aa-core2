import subprocess
from aacore.sniffers import sniffer

from django.template import Context
from django.template.loader import get_template

try: import simplejson as json
except ImportError: import json


@sniffer("application/ogg")
class OggSniffer(object):
    def sniff(self, url):
        print("sniffed an ogg file")
        print(url)
        cmd = ['ffprobe', '-show_format', '-print_format', 'json', '-loglevel', 'quiet', url]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err =  p.communicate()
        t = get_template("aacore/ogg.html")
        c = Context({"url": url})
        c.update(json.loads(out))
        print(out)
        return t.render(c)
