from aacore.sniffers import sniffer
import RDF


@sniffer("rdfa")
class HtmlSniffer(object):
    def test(self, model):
        q = '''
        PREFIX aa: <http://activearchives.org/terms/>
        ASK {
            { ?a aa:content-type "text/html" .}
            UNION
            { ?a aa:mime-type "text/html" .}
        }'''
        results = RDF.Query(q, query_language="sparql").execute(model)
        return results.get_boolean()

    def sniff(self, url):
        print("sniffed an html page")
        print(url)
