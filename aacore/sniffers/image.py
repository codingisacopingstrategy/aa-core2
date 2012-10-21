from aacore.sniffers import sniffer
import RDF


@sniffer("rdfa")
class ImageSniffer(object):
    def test(self, model):
        q = '''
        PREFIX aa: <http://activearchives.org/terms/>
        ASK {
            { ?a aa:content-type ?ct. }
            UNION
            { ?a aa:mime-type ?ct. }
            FILTER (REGEX(?ct, "^image/")).
        }'''
        results = RDF.Query(q, query_language="sparql").execute(model)
        return results.get_boolean()

    def sniff(self, url):
        print("sniffed an image")
        print(url)
        return "ok"
