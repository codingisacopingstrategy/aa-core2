from aacore.sniffers import sniffer
import RDF


@sniffer("rdfa")
class HtmlSniffer(object):
    def __init__(self, request=None, model=None):
        self.request = request
        self.model = model

    def test(self):
        q = '''
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX hdr: <http://www.w3.org/2011/http-headers#>
        ASK {
            { ?subject dct:format "text/html" .}
            UNION
            { ?subject hdr:content-type ?object .}
            FILTER (REGEX(?object, "^text/html")).
        }'''
        results = RDF.Query(q, query_language="sparql").execute(self.model)
        return results.get_boolean()

    def sniff(self):
        print("sniffed an html page")
        return self.request.text
