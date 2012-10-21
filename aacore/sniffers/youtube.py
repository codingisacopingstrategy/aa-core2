from aacore.sniffers import sniffer
import RDF


@sniffer("rdfa")
class YoutubeSniffer(object):
    def test(self, model):
        q = '''
        PREFIX aa: <http://activearchives.org/terms/>
        ASK {
            { ?subject aa:content-type "text/html" .}
            UNION
            { ?subject aa:mime-type "text/html" .}

            FILTER (REGEX(str(?subject), "^http://www.youtube")).
        }'''
        results = RDF.Query(q, query_language="sparql").execute(model)
        return results.get_boolean()

    def sniff(self, url):
        print("sniffed an youtube page")
        print(url)
        return "ok"
