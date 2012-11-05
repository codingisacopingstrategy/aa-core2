from aacore.sniffers import sniffer
import RDF


@sniffer("rdfa")
class ImageSniffer(object):
    def __init__(self, resource):
        self.resource = resource

    def test(self):
        q = '''
        PREFIX aa: <http://activearchives.org/terms/>
        ASK {
            { ?a aa:content-type ?ct. }
            UNION
            { ?a aa:mime-type ?ct. }
            FILTER (REGEX(?ct, "^image/")).
        }'''
        results = RDF.Query(q, query_language="sparql").execute(self.resource.dummy_model)
        return results.get_boolean()

    def sniff(self):
        print("sniffed an image")
        print(self.resource.url)
        return "ok"
