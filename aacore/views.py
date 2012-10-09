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


from django.shortcuts import render
from django.shortcuts import (render_to_response, get_object_or_404)
from django.http import HttpResponseRedirect
from django.template import RequestContext 

from forms import ResourceForm
from rdfindex import AAResource 
import RDF


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

        print(node)
        query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT ?predicate ?object
            WHERE {
                <%s> ?predicate ?object .
            }
        """ % node

        storage_dir = "/tmp"
        storage_name = "aa"

        options = "hash-type='bdb', contexts='yes', dir='%s'" % storage_dir
        storage = RDF.HashStorage(storage_name, options=options)
        model = RDF.Model(storage)

        rdf_results = RDF.Query(query.encode("utf-8"), query_language="sparql").execute(model)

        results = []

        for result in rdf_results:
            results.append(result)
        #import pdb; pdb.set_trace()

        form = ResourceForm()
        return render_to_response("aacore/browse.html", {"form": form, "results": results}, 
                                  context_instance=RequestContext(request))

