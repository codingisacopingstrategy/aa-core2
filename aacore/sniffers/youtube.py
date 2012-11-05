from aacore.sniffers import sniffer
import RDF


@sniffer("rdfa")
class YoutubeSniffer(object):
    def __init__(self, resource):
        self.resource = resource

    def test(self):
        q = '''
        PREFIX aa: <http://activearchives.org/terms/>
        ASK {
            { ?subject aa:content-type "text/html" .}
            UNION
            { ?subject aa:mime-type "text/html" .}

            FILTER (REGEX(str(?subject), "^http://www.youtube")).
        }'''
        results = RDF.Query(q, query_language="sparql").execute(self.resource.dummy_model)
        return results.get_boolean()

    def sniff(self):
        print("sniffed an youtube page")
        print(self.resource.url)
        return "ok"
