# This file is part of Active Archives.
# Copyright 2006-2011 the Active Archives contributors (see AUTHORS)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Also add information on how to contact you by electronic and paper mail.


"""
Active Archives aacore views
"""

import RDF

from django.shortcuts import render
from django.shortcuts import (render_to_response, get_object_or_404)
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext 
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied

from forms import ResourceForm
from aacore import RDF_MODEL
from aacore.models import Namespace
from aacore.sniffers import AAResource 
from rdfutils import load_links
from urlparse import urlparse


def browse(request):
    node = request.REQUEST.get("node")
    do_reload = request.REQUEST.get("_submit") == "reload"

    # If nothing is browsed, simply return an empty form
    if not node:
        form = ResourceForm()
        return render_to_response("aacore/browse.html", {"form": form}, 
                                  context_instance=RequestContext(request))
    else:
        AAResource(node).index()

        # RDF distinguishes URI and literals...
        is_literal = urlparse(node).scheme not in ('file', 'http', 'https')
        #print(load_links(RDF_MODEL, node, literal=is_literal))

        #print(node)
        query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT ?predicate ?object
            WHERE {
                <%s> ?predicate ?object .
            }
        """ % node

        rdf_results = RDF.Query(query.encode("utf-8"), query_language="sparql").execute(RDF_MODEL)

        results = []

        for result in rdf_results:
            results.append(result)

        form = ResourceForm()
        return render_to_response("aacore/browse.html", {"node": node, "form": form, "results": results}, 
                                  context_instance=RequestContext(request))

@csrf_exempt
@require_http_methods(["POST"])
def sparql(request):
    """
    Implement a simple SPARQL endpoint, accessible through POST requests.
    
    > Protocol clients may send protocol requests via the HTTP POST method
    > by including the query directly and unencoded as the HTTP request
    > message body.  [1] 
    
    Sends back Sparql results in an XML serialisation,
    with mime/type application/sparql-results+xml [2]
    
    [1] http://www.w3.org/TR/sparql11-protocol/#query-via-post-direct 
    [2] http://www.w3.org/TR/rdf-sparql-XMLres/#mime
    """
    if request.META['CONTENT_TYPE'] == 'application/sparql-query':
        query = request.body
        rdf_results = RDF.Query(query.encode("utf-8"), query_language="sparql").execute(RDF_MODEL)
        return HttpResponse(rdf_results.to_string(), mimetype="application/sparql-results+xml")
    else:
        raise PermissionDenied

def namespaces_css (request):
    """
    Generates a stylesheet with the namespace colors.

    **Context**

    ``RequestContext``

    ``namespaces``
        A queryset of all :model:`aacore.Namespace`.

    **Template:**

    :template:`aacore/namespaces.css`
    """
    context = {}
    context['namespaces'] = Namespace.objects.all()
    return render_to_response("aacore/namespaces.css", context, 
                              context_instance=RequestContext(request), mimetype="text/css")


